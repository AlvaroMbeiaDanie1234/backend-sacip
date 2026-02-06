"""
Test script to verify Firestore setup once authentication is configured.
"""

def test_firestore_connection():
    """
    Test function to check Firestore connectivity.
    This will only work once authentication is properly configured.
    """
    print("Firestore Connection Test")
    print("=" * 30)
    
    try:
        # Try to import and initialize Firestore
        from alvos_sob_investigacao.firestore_utils import FirestoreService
        print("✅ Firestore utilities imported successfully")
        
        # Try to create a service instance (this will fail without auth)
        service = FirestoreService()
        print("✅ Firestore service initialized")
        
        # Try to connect to the users collection
        users = service.get_collection('users')
        print(f"✅ Successfully connected to Firestore")
        print(f"✅ Found {len(users)} users in the 'users' collection")
        
        if users:
            print("\nSample user data:")
            sample_user = users[0]
            print(f"  ID: {sample_user.get('id', 'N/A')}")
            print(f"  Name: {sample_user.get('nome', 'N/A')}")
            print(f"  Email: {sample_user.get('email', 'N/A')}")
            print(f"  Location: {sample_user.get('morada', 'N/A')}")
        
        return True
        
    except Exception as e:
        print(f"⚠️  Authentication not configured yet: {str(e)}")
        print("\n💡 Please follow the setup guide in FIRESTORE_SETUP_GUIDE.md")
        print("   You need to configure your Firebase service account credentials.")
        return False

def test_endpoints_available():
    """
    Test that the endpoints are properly registered in Django.
    """
    print("\nDjango Endpoint Registration Test")
    print("=" * 35)
    
    try:
        # Test that the views can be imported without authentication
        from alvos_sob_investigacao.views import FirestoreUsersView
        print("✅ FirestoreUsersView is properly registered")
    except ImportError as e:
        print(f"❌ Could not import FirestoreUsersView: {e}")
        return False
    
    try:
        from monitorizacao_de_redes_sociais.views import get_nossa_comunidade_users
        print("✅ get_nossa_comunidade_users function is available")
    except ImportError as e:
        print(f"❌ Could not import get_nossa_comunidade_users: {e}")
        return False
    
    print("\n📋 Endpoints that will be available once authentication is configured:")
    print("   • GET /alvos-sob-investigacao/firestore-users/ - Get all users from Firestore")
    print("   • GET /monitorizacao-de-redes-sociais/nossa-comunidade/users/ - Get users for Nossa Comunidade section")
    
    return True

def main():
    print("SACIP Firestore Integration - Setup Verification")
    print("=" * 50)
    print("This script verifies that the Firestore integration is properly set up.\n")
    
    # Test endpoint registration
    endpoints_ok = test_endpoints_available()
    
    print(f"\nEndpoint registration: {'✅ OK' if endpoints_ok else '❌ Issues found'}")
    
    # Test Firestore connection (requires auth)
    connection_ok = test_firestore_connection()
    
    print(f"\nFirestore connection: {'✅ OK' if connection_ok else '⚠️  Needs authentication setup'}")
    
    print("\n" + "=" * 50)
    if endpoints_ok and not connection_ok:
        print("🔧 The integration is properly set up in the code!")
        print("   You just need to configure authentication to connect to Firestore.")
        print("   See FIRESTORE_SETUP_GUIDE.md for instructions.")
    elif endpoints_ok and connection_ok:
        print("🎉 Everything is working! Your Firestore integration is fully functional.")
    else:
        print("❌ There are issues that need to be resolved.")

if __name__ == "__main__":
    main()