def set_sidc_identity(sidc: str, identity: str) -> str:
    '''
    Set the identity of the SIDC (the third and fourth characters)
    '''
    assert len(identity) in [1, 2], 'Identity must be a single character or a pair of characters'
    identity = identity.rjust(2, '0')
    return sidc[:2] + identity + sidc[4:]
