def set_sidc_identity(sidc: str, identity: str) -> str:
    '''
    Set the identity of the SIDC (the third and fourth characters)
    '''
    assert len(identity) in [1, 2], 'Identity must be a single character or a pair of characters'
    identity = identity.rjust(2, '0')
    return sidc[:2] + identity + sidc[4:]

def get_sidc_identity_from_color(color: str | None) -> str:
    '''
    Get APP-6(D) identity from a color.
    TODO: add more colors
    '''
    match (color or '').lower():
        case 'red' | '#9d2400': return '6'
        case 'green' | '#00ff00': return '4'
        case 'blue' | '#00ffff' | '#0f78ff': return '3'
        case _: return '1'
    
