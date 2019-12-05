import random

def normalize_flow(flow):
    # Grab the low end of the resting reading
    base = 256
    
    zero_val = base - 2

    ref_val = zero_val - flow
    
    if ref_val <= 0:
        return 0
    
    if ref_val < 15:
        # pegged to top of reading
        return_val = ref_val * 7
    else:
        return 100

    return_val = return_val + random.randint(-3, 3)

    if return_val < 0:
        return 0
    if return_val > 100:
        return 100

    return return_val 

def normalize_volume(vol):
    # Grab the low end of the resting reading
    base = 825
    
    zero_val = base - 25

    ref_val = zero_val - vol
    
    if ref_val <= 0:
        return 0
    
    if ref_val < 164:
        # pegged to 2000 mL, (ref_val - 2000 mL reading)
        return_val = (ref_val ** 2.8) / 796
    elif ref_val < 168:
        # pegged to less than 2500 mL, (ref_val - 2500 mL reading)
        return_val = ((168 - ref_val) * 125) + 1500
    else:
        return 2500

    return_val = return_val + random.randint(-5, 5)

    if return_val < 0:
        return 0
    if return_val > 2500:
        return 2500

    return return_val 


print(normalize_volume(825))
print(normalize_volume(805))
print(normalize_volume(700))
print(normalize_volume(665))
print(normalize_volume(650))
print(normalize_volume(636))
print(normalize_volume(631))
