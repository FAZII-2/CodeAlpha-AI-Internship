import json
import re
from dataclasses import dataclass, field

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from backend.app.config import (
    FAQ_DATA_DIR,
    CONFIDENT_THRESHOLD,
    SUGGESTION_THRESHOLD,
    MAX_SUGGESTIONS,
)
from backend.app.nlp.preprocessing import clean_text, build_matching_text
from backend.app.nlp.calculators import try_calculate

@dataclass
class FAQEntry:
    id: int
    category: str
    question: str
    answer: str
    alternate_questions: list[str] = field(default_factory=list)
    keywords: list[str] = field(default_factory=list)


@dataclass
class MatchResult:
    answer: str | None
    confidence: float
    matched_question: str | None
    category: str | None
    is_fallback: bool
    suggestions: list[dict] = field(default_factory=list)


class FAQMatcher:
    
    def __init__(self) -> None:
        self.entries: list[FAQEntry] = []
        self.vectorizer: TfidfVectorizer | None = None
        self.faq_vectors = None
        self._load_entries()
        self._build_vectors()

    def _load_entries(self) -> None:
        next_id = 1
        for file_path in sorted(FAQ_DATA_DIR.glob("*.json")):
            with open(file_path, encoding="utf-8") as f:
                data = json.load(f)

            category = data["category"]
            for faq in data["faqs"]:
                self.entries.append(
                    FAQEntry(
                        id=next_id,
                        category=category,
                        question=faq["question"],
                        answer=faq["answer"],
                        alternate_questions=faq.get("alternate_questions", []),
                        keywords=faq.get("keywords", []),
                    )
                )
                next_id += 1

        if not self.entries:
            raise RuntimeError(f"No FAQ entries found in {FAQ_DATA_DIR}")

    def _build_vectors(self) -> None:
        matching_texts = [
            build_matching_text(e.question, e.alternate_questions, e.keywords)
            for e in self.entries
        ]

        self.vectorizer = TfidfVectorizer()
        self.faq_vectors = self.vectorizer.fit_transform(matching_texts)

    def match(self, user_message: str) -> MatchResult:
        conversation_result = self._match_conversation(user_message)
        if conversation_result is not None:
            return conversation_result

        cleaned = clean_text(user_message)

        if not cleaned:
            return MatchResult(
                answer="Could you rephrase your question? I didn't catch any words to work with.",
                confidence=0.0,
                matched_question=None,
                category=None,
                is_fallback=True,
            )

        calc_result = try_calculate(user_message)
        if calc_result is not None:
            return MatchResult(
                answer=calc_result.answer,
                confidence=1.0,
                matched_question=None,
                category="Calculator",
                is_fallback=False,
            )
        
        user_vector = self.vectorizer.transform([cleaned])
        scores = cosine_similarity(user_vector, self.faq_vectors)[0]

        best_index = scores.argmax()
        best_score = float(scores[best_index])
        best_entry = self.entries[best_index]

        if best_score >= CONFIDENT_THRESHOLD:
            return MatchResult(
                answer=best_entry.answer,
                confidence=best_score,
                matched_question=best_entry.question,
                category=best_entry.category,
                is_fallback=False,
            )

        if best_score >= SUGGESTION_THRESHOLD:
            top_indices = scores.argsort()[::-1][:MAX_SUGGESTIONS]
            suggestions = [
                {
                    "question": self.entries[i].question,
                    "category": self.entries[i].category,
                    "confidence": float(scores[i]),
                }
                for i in top_indices
            ]
            return MatchResult(
                answer="I'm not fully sure what you're asking. Did you mean one of these?",
                confidence=best_score,
                matched_question=None,
                category=None,
                is_fallback=True,
                suggestions=suggestions,
            )

        return MatchResult(
            answer="I couldn't find a good match for that. Could you rephrase your question, "
            "or ask about accounts, cards, transfers, loans, online banking, security, or fees?",
            confidence=best_score,
            matched_question=None,
            category=None,
            is_fallback=True,
        )

    def _match_conversation(self, user_message: str) -> MatchResult | None:
        normalized = re.sub(r"[^a-z0-9']+", " ", user_message.lower()).strip()
        if not normalized:
            return None

        conversation_responses = [
            (
                r"^(hello|hi|hey|hiya|good morning|good afternoon|good evening|greetings)( there)?$",
                "Hello! I'm here to help with banking questions about accounts, cards, transfers, loans, online banking, security, and fees. What would you like to know?",
            ),
            (
                r"^(how are you|how are you doing|hope you are well)$",
                "I'm BankID, and I'm ready to help with your banking questions. You can ask about accounts, cards, transfers, loans, fees, or online banking.",
            ),
            (
                r"^(thanks|thank you|thank you so much|thanks a lot|much appreciated|appreciate it)$",
                "You're welcome! Let me know if you have another banking question.",
            ),
            (
                r"^(bye|goodbye|see you|see you later|that is all|that's all|i am done|i'm done)$",
                "Goodbye! Feel free to come back whenever you have a banking question.",
            ),
            (
                r"^(help|i need help|can you help me|please help|i have a question)$",
                "I can help with general questions about accounts, cards, transfers, loans, online banking, security, fees, and banking terms. What would you like to ask?",
            ),
            (
                r"^(hello|hi|hey)( there)? (can you help me|please help|i need help)$",
                "I can help with general questions about accounts, cards, transfers, loans, online banking, security, fees, and banking terms. What would you like to ask?",
            ),
            (
                r"^(who are you|are you a bot|are you ai|are you a real person)$",
                "I'm BankID, an automated assistant for general banking questions. I can't access personal accounts, balances, passwords, or transactions, so use your bank's official app or support team for account-specific help.",
            ),
            (
                r"^(what is your name|what's your name|whats your name|your name|what should i call you|tell me your name|what is bankid|what's bankid)$",
                "My name is BankID. I can help with general banking questions, but I cannot access your personal account.",
            ),
            (
                r"^(can i talk to a human|i need a human|connect me to an agent|speak to customer service|i want a real person)$",
                "I can't transfer chats directly, but your bank's official customer support team can help with account-specific or urgent issues. Use the phone number on your card or the official bank app.",
            ),
            (
                r"^(can you access my account|can you check my balance|do you know my balance|can you see my transactions)$",
                "No. BankID cannot access accounts, balances, passwords, PINs, OTPs, or transaction records. Use your bank's official app or contact its verified support team.",
            ),
            (
                r"^(is my information safe|are you safe to use|what about privacy|do you store my data)$",
                "Do not share passwords, PINs, OTPs, full card numbers, or other sensitive information here. For account security or privacy details, use your bank's official privacy policy and support channels.",
            ),
            (
                r"^(what topics can you answer|what questions can i ask|what can bankid do|what do you know)$",
                "BankID can explain accounts, cards, transfers, payments, loans, credit, fees, online banking, security, fraud, and common banking terms. It can also estimate EMI and savings calculations.",
            ),
            (
                r"^(can you speak another language|do you support other languages|can i use voice input)$",
                "BankID currently provides English text answers and browser-based English voice input where supported. You can type your question whenever voice input is unavailable.",
            ),
        ]

        for pattern, answer in conversation_responses:
            if re.fullmatch(pattern, normalized):
                return MatchResult(
                    answer=answer,
                    confidence=1.0,
                    matched_question=None,
                    category="Assistant",
                    is_fallback=False,
                )

        return None

    def match_with_context(self, user_message: str, recent_messages: list[str] | None = None) -> MatchResult:
        
        result = self.match(user_message)

        if not result.is_fallback or not recent_messages:
            return result

        last_message = recent_messages[-1] if recent_messages else ""
        if not last_message:
            return result

        combined = f"{last_message} {user_message}"
        context_result = self.match(combined)

        if context_result.confidence > result.confidence:
            return context_result

        return result


# One shared instance the rest of the app imports and reuses.
faq_matcher = FAQMatcher()