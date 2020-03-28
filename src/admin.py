'''
File for admin related functions
'''

from data import get_data
import authenticate as au

@au.authenticator(au.is_admin, au.check_u_id_existence, au.is_valid_permission_id)
def admin_userpermission_change(*, token, u_id, permission_id):
    '''
    Given a User by their user ID, 
    set their permissions to new permissions described by permission_id
    '''
    user = get_data().get_user_with_u_id(u_id)
    user.set_permission_id(permission_id)
    return {}