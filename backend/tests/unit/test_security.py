from app.core.security import hash_password, verify_password, create_access_token, decode_token


class TestPasswordHashing:
    def test_hash_and_verify(self):
        password = "SecurePass123!"
        hashed = hash_password(password)
        assert hashed != password
        assert verify_password(password, hashed) is True

    def test_verify_wrong_password(self):
        hashed = hash_password("correct")
        assert verify_password("wrong", hashed) is False


class TestJWT:
    def test_create_and_decode_access_token(self):
        token = create_access_token(data={"sub": "test-user-id", "email": "test@test.com"})
        payload = decode_token(token)
        assert payload is not None
        assert payload["sub"] == "test-user-id"
        assert payload["email"] == "test@test.com"
        assert payload["type"] == "access"

    def test_decode_invalid_token(self):
        payload = decode_token("not.a.valid.token")
        assert payload is None
