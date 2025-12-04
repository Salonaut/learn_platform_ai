"""
DEPRECATED: This file has been split into separate test files.

Please use the following test files instead:
- test_registration_serializer.py - Tests for UserRegistrationSerializer
- test_login_serializer.py - Tests for UserLoginSerializer
- test_profile_serializer.py - Tests for UserProfileSerializer
- test_update_serializer.py - Tests for UserUpdateSerializer
- test_change_password_serializer.py - Tests for UserChangePasswordSerializer

This file is kept for reference but should not be used.
All tests have been rewritten according to best practices:
- Using real User instances instead of MagicMock
- Parameterized repetitive tests
- Split into separate files for clarity
- Using factories (factory_boy) for efficient test data creation
- Proper patch paths for mocks
- Asserting error keys/codes instead of exact messages
- Added negative and edge-case tests
- Testing read_only/write_only fields
- Verifying serializer return values and side effects
"""
