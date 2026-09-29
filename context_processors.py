def user_identity_flags(request):
    return {
        'is_patient': request.session.get('is_patient', False),
        'is_manager': request.session.get('is_manager', False),
    }
