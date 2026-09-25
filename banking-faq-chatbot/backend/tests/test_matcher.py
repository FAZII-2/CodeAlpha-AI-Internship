import pytest

from backend.app.nlp.matcher import faq_matcher


class TestConfidentMatches:
    """Questions phrased close to how the FAQ data is written should match confidently."""

    def test_open_account(self):
        result = faq_matcher.match("How do I open a bank account?")
        assert not result.is_fallback
        assert result.category == "Accounts"

    def test_block_card(self):
        result = faq_matcher.match("How do I block my debit card?")
        assert not result.is_fallback
        assert "block" in result.matched_question.lower()

    def test_credit_score(self):
        result = faq_matcher.match("What is a credit score?")
        assert not result.is_fallback
        assert result.category == "Loans and Credit"


class TestParaphrasedMatches:
    """Real users rarely use exact FAQ wording; alternates should still work."""

    def test_lost_card_paraphrase(self):
        result = faq_matcher.match("I lost my ATM card, what do I do?")
        assert not result.is_fallback
        assert "block" in result.matched_question.lower() or "card" in result.matched_question.lower()

    def test_swift_code_short(self):
        result = faq_matcher.match("swift code")
        assert not result.is_fallback


class TestFallbackBehavior:
    """Off-topic or nonsense questions must not get a confident wrong answer."""

    def test_offtopic_question(self):
        result = faq_matcher.match("what's the weather like today")
        assert result.is_fallback
        assert result.confidence < 0.3

    def test_empty_message(self):
        result = faq_matcher.match("")
        assert result.is_fallback

    def test_greeting_is_handled_by_assistant(self):
        result = faq_matcher.match("hello there")
        assert not result.is_fallback
        assert result.category == "Assistant"
        assert "banking" in result.answer.lower()

    def test_informal_help_request_is_handled(self):
        result = faq_matcher.match("hey, can you help me?")
        assert not result.is_fallback
        assert result.category == "Assistant"

    def test_thanks_is_handled(self):
        result = faq_matcher.match("thanks a lot")
        assert not result.is_fallback
        assert result.category == "Assistant"

    def test_assistant_name_is_bankid(self):
        result = faq_matcher.match("what is your name?")
        assert not result.is_fallback
        assert result.category == "Assistant"
        assert "BankID" in result.answer

    def test_contracted_assistant_name_question_is_handled(self):
        result = faq_matcher.match("what's your name?")
        assert not result.is_fallback
        assert "BankID" in result.answer

    def test_account_access_boundary_is_clear(self):
        result = faq_matcher.match("can you check my balance?")
        assert not result.is_fallback
        assert "cannot access" in result.answer


class TestCalculators:
    """Calculator questions should compute real numbers, not return FAQ text."""

    def test_emi_calculation(self):
        result = faq_matcher.match("EMI on 300000 at 10 percent for 2 years")
        assert result.category == "Calculator"
        assert not result.is_fallback
        assert "13,843" in result.answer or "13843" in result.answer

    def test_savings_calculation(self):
        result = faq_matcher.match("if I save 10000 at 6% for 5 years how much will I have")
        assert result.category == "Calculator"
        assert not result.is_fallback

    def test_labeled_amount_can_appear_after_rate_and_term(self):
        result = faq_matcher.match("loan at 10% for 2 years amount 300000")
        assert result.category == "Calculator"
        assert "13,843" in result.answer or "13843" in result.answer

    def test_invalid_emi_duration_falls_back(self):
        result = faq_matcher.match("EMI for 300000 at 10% for 0 years")
        assert result.is_fallback


class TestContext:
    """A weak short message should be rescued by the previous message's context."""

    def test_followup_after_block_card(self):
        result = faq_matcher.match_with_context(
            "and how do i get a new one",
            recent_messages=["How do I block my debit or credit card?"],
        )
        assert not result.is_fallback
        assert "replace" in result.answer.lower() or "new card" in result.matched_question.lower()


class TestDataIntegrity:
    """Sanity checks on the loaded dataset itself."""

    def test_faqs_loaded(self):
        assert len(faq_matcher.entries) >= 80

    def test_every_entry_has_an_answer(self):
        assert all(entry.answer.strip() for entry in faq_matcher.entries)

    def test_every_entry_has_a_category(self):
        assert all(entry.category.strip() for entry in faq_matcher.entries)