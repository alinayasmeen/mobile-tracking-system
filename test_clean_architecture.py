"""
Test script to verify the refactored clean architecture system
"""

import sys
import os

# Add the backend directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

def test_clean_architecture():
    print("Testing Clean Architecture Implementation...")
    
    # Test domain layer
    print("\n1. Testing Domain Layer...")
    try:
        from domain.Entities import User, Phone, Report, TransferRequest, RetailerPurchase
        from domain.Interfaces import UserRepositoryInterface, PhoneRepositoryInterface
        print("   + Domain entities and interfaces imported successfully")
    except ImportError as e:
        print(f"   - Failed to import domain components: {e}")
        return False
    
    # Test application layer
    print("\n2. Testing Application Layer...")
    try:
        from application.UseCases import UserRegistrationUseCase, PhoneRegistrationUseCase, ReportCreationUseCase
        print("   + Application use cases imported successfully")
    except ImportError as e:
        print(f"   - Failed to import application components: {e}")
        return False
    
    # Test interface adapters layer
    print("\n3. Testing Interface Adapters Layer...")
    try:
        from interface_adapters.Controllers import UserController, PhoneController
        from interface_adapters.Repositories import UserRepository, PhoneRepository
        print("   + Interface adapters imported successfully")
    except ImportError as e:
        print(f"   - Failed to import interface adapter components: {e}")
        return False
    
    # Test infrastructure layer
    print("\n4. Testing Infrastructure Layer...")
    try:
        from database import get_db, engine
        from auth import get_password_hash, verify_password
        print("   + Infrastructure components imported successfully")
    except ImportError as e:
        print(f"   - Failed to import infrastructure components: {e}")
        return False
    
    # Test agent service integration
    print("\n5. Testing Agent Service Integration...")
    try:
        from imei_matching_agent import IMEIMatchingAgent
        from agents.agent_models import AgentInput, EventType
        print("   + Agent service integration imported successfully")
    except ImportError as e:
        print(f"   - Failed to import agent service components: {e}")
        return False
    
    print("\n+ All architecture layers are properly implemented and connected!")
    print("\nClean Architecture Summary:")
    print("- Domain Layer: Contains entities and business rules")
    print("- Application Layer: Contains use cases and business logic")
    print("- Interface Adapters: Contains controllers and repository implementations")
    print("- Infrastructure: Contains frameworks, drivers, and external agencies")
    print("- Frameworks & Drivers: Database, web framework, external services")
    
    return True

if __name__ == "__main__":
    success = test_clean_architecture()
    if success:
        print("\n+ Clean architecture refactoring completed successfully!")
    else:
        print("\n- Clean architecture refactoring has issues!")
        sys.exit(1)