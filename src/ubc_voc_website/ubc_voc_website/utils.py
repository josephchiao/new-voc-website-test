from membership.models import Exec

def is_exec(user):
    """
    Same functionality as the Execs decorator,
    but allows for use beyond basic access control
    """
    return Exec.objects.filter(user=user).exists()