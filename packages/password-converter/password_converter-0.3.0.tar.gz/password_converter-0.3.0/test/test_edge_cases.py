from password_converter.converter import convert_text

def test_empty_input():
    result = convert_text("")
    assert len(result) == 0

def test_malformed_input():
    malformed_text = """
    Invalid format
    No proper keys
    ---
    Also invalid
    """
    result = convert_text(malformed_text)
    assert len(result) == 0

def test_special_characters():
    text = """Website name: example™
Website URL: https://example.com/™
Login: user™@example.com
Password: pass™word123
Comment: Test™ account
---"""
    result = convert_text(text)
    assert len(result) == 1
    assert "™" in result[0]["Title"]
    assert "™" in result[0]["URL"]
    assert "™" in result[0]["Username"]
    assert "™" in result[0]["Password"]
    assert "™" in result[0]["Notes"]

def test_extra_fields():
    text = """Website name: example.com
Website URL: https://example.com
Login: user@example.com
Password: secretpass
ExtraField1: something
ExtraField2: something else
Comment: Test account
---"""
    result = convert_text(text)
    assert len(result) == 1
    # Extra fields should be ignored
    assert "ExtraField1" not in result[0]
    assert "ExtraField2" not in result[0]

def test_missing_separator():
    text = """Website name: site1.com
Website URL: https://site1.com
Login: user1
Password: pass1
Website name: site2.com
Website URL: https://site2.com
Login: user2
Password: pass2"""
    result = convert_text(text)
    # Should still parse as one entry
    assert len(result) == 1

def test_multiple_separators():
    text = """Website name: example.com
Website URL: https://example.com
Login: user@example.com
Password: secretpass
---
---
---
Application: TestApp
Login: testuser
Password: apppass123"""
    result = convert_text(text)
    assert len(result) == 2  # Multiple separators should be treated as one

def test_unicode_handling():
    text = """Website name: 例子.com
Website URL: https://例子.com
Login: 用户@例子.com
Password: 密码123
Comment: テスト
---"""
    result = convert_text(text)
    assert len(result) == 1
    assert "例子.com" in result[0]["Title"]
    assert "例子.com" in result[0]["URL"]
    assert "用户" in result[0]["Username"]
    assert "密码" in result[0]["Password"]
    assert "テスト" in result[0]["Notes"]