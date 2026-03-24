from rest_framework import status, generics, permissions
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from .models import User, Role, OrganizationalUnit, MenuPermission
from .serializers import UserSerializer, UserRegistrationSerializer, LoginSerializer, RoleSerializer, OrganizationalUnitSerializer, MenuPermissionSerializer


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def register_user(request):
    """
    Register a new user
    """
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        # Check if organizational unit exists
        org_unit_id = request.data.get('organizational_unit')
        if org_unit_id:
            try:
                org_unit = OrganizationalUnit.objects.get(id=org_unit_id)
            except OrganizationalUnit.DoesNotExist:
                return Response({
                    'error': 'Organizational unit not found'
                }, status=status.HTTP_400_BAD_REQUEST)
        
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'user': UserSerializer(user).data,
            'token': token.key
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login_user(request):
    """
    Authenticate and login a user
    """
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        user = authenticate(email=email, password=password)
        
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'user': UserSerializer(user).data,
                'token': token.key
            })
        else:
            return Response({
                'error': 'Invalid credentials'
            }, status=status.HTTP_401_UNAUTHORIZED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def logout_user(request):
    """
    Logout a user by deleting their token
    """
    try:
        # Check if user has an auth token before trying to delete it
        if hasattr(request.user, 'auth_token'):
            request.user.auth_token.delete()
        return Response({'message': 'Logged out successfully'}, status=status.HTTP_200_OK)
    except Exception as e:
        # Log the error but still return success to prevent hanging
        print(f"Logout error: {str(e)}")
        # Still clear local storage on client side
        return Response({'message': 'Logged out successfully'}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def list_organizational_units(request):
    """
    List all organizational units
    """
    org_units = OrganizationalUnit.objects.all()
    serializer = OrganizationalUnitSerializer(org_units, many=True)
    return Response(serializer.data)


class UserListView(generics.ListCreateAPIView):
    """
    List all users or create a new user
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = []  # Disables token check completely
    permission_classes = [permissions.AllowAny]  # Removed authentication requirement


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a user instance
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class RoleListView(generics.ListCreateAPIView):
    """
    List all roles or create a new role
    """
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [permissions.AllowAny]


class RoleDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a role instance
    """
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [permissions.AllowAny]


class MenuPermissionListView(generics.ListCreateAPIView):
    """
    List all menu permissions or create a new menu permission
    """
    queryset = MenuPermission.objects.all()
    serializer_class = MenuPermissionSerializer
    authentication_classes = []  # Disables token check completely
    permission_classes = [permissions.AllowAny]  # Removed authentication requirement


class MenuPermissionDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a menu permission instance
    """
    queryset = MenuPermission.objects.all()
    serializer_class = MenuPermissionSerializer
    permission_classes = [permissions.IsAuthenticated]


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def assign_menu_permissions(request, user_id):
    """
    Assign menu permissions to a user
    """
    try:
        user = User.objects.get(id=user_id)
        permission_ids = request.data.get('menu_permission_ids', [])
        menu_permissions = MenuPermission.objects.filter(id__in=permission_ids)
        user.menu_permissions.set(menu_permissions)
        return Response({'message': 'Menu permissions assigned successfully'}, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_user_menu_permissions(request, user_id):
    """
    Get menu permissions for a user
    """
    try:
        user = User.objects.get(id=user_id)
        serializer = MenuPermissionSerializer(user.menu_permissions.all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_current_user(request):
    """
    Get current authenticated user's information
    """
    try:
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)