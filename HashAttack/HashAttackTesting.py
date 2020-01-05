# python modules
import numpy as np
import random
import matplotlib.pyplot as plt

# local files
from HashAttack.CroppedHashTools import *

if __name__ == '__main__':
    # value for how many samples of each attack at each bit value
    iterations = 50
    # bit lengths to test
    bit_lengths = [4, 8, 12, 16, 20]
    # collision_results is a dictionary with key of bit length to an array of lists ordered as:
    # [ number of hashes before a collision was found, found collision value ]
    collision_results = {}
    # pre_image_results is a dictionary with key of bit length to an array of lists ordered as:
    # [ number of hashes before a collision was found with pre-selected random value, pre-selected value ]
    pre_image_results = {}

    # Run Attacks on all bit lengths in list
    for length in bit_lengths:
        # Collision Attack
        for _ in range(iterations):
            count = 0
            hash_input = random.randint(0, (2**64) - 1)
            hash_results = set()
            while 1:
                count += 1
                hash_input += 1
                new_hash = hash_string_to_crop(str(hash_input), length)
                if new_hash in hash_results:
                    if str(length) in collision_results.keys():
                        collision_results[str(length)].append([count, new_hash])
                    else:
                        collision_results[str(length)] = [[count, new_hash]]
                    break
                else:
                    hash_results.add(new_hash)

        # Pre-Image Attack
        for _ in range(iterations):
            random_pre_image = hash_string_to_crop(str(random.randint(0, (2**64) - 1)), length)
            count = 0
            hash_input = random.randint(0, (2**64) - 1)
            while 1:
                count += 1
                hash_input += 1
                new_hash = hash_string_to_crop(str(hash_input), length)
                if new_hash == random_pre_image:
                    if str(length) in pre_image_results.keys():
                        pre_image_results[str(length)].append([count, new_hash])
                    else:
                        pre_image_results[str(length)] = [[count, new_hash]]
                    break

    # calculate averages for each bit length
    collision_y_plots = []
    pre_image_y_plots = []
    for key in collision_results.keys():
        collision_y_plots.append(np.array([collision_results[key][index][0]
                                           for index in range(0, len(collision_results[key]))]).mean())
    for key in pre_image_results.keys():
        pre_image_y_plots.append(np.array([pre_image_results[key][index][0]
                                           for index in range(0, len(pre_image_results[key]))]).mean())

    # Create graphs
    theoretical_collisions = [2**(l/2) for l in bit_lengths]
    plt.plot(bit_lengths, collision_y_plots, color='blue', lw=2, label="Actual")
    plt.plot(bit_lengths, theoretical_collisions, color='red', lw=1, label="Theoretical [ 2^(n/2) ]")
    plt.yscale('log')
    plt.title('Average Attempts at Collision Attack per Bit Length')
    plt.xlabel('Bit Lengths')
    plt.ylabel('Average # Attempts per 50 rounds')
    plt.legend()
    plt.show()

    theoretical_pre_image = [2**l for l in bit_lengths]
    plt.plot(bit_lengths, pre_image_y_plots, color='blue', lw=2, label='Actual')
    plt.plot(bit_lengths, theoretical_pre_image, color='red', lw=1, label='Theoretical [ 2^n ]')
    plt.yscale('log')
    plt.title('Average Attempts at Pre-Image Attack per Bit Length')
    plt.xlabel('Bit Lengths')
    plt.ylabel('Average # Attempts per 50 rounds')
    plt.legend()
    plt.show()

    print(f'Theoretical Collisions: {theoretical_collisions}')
    print(f'Actual Collisions:      {collision_y_plots}')
    print(f'Bit Lengths:            {bit_lengths}\n')

    print(f'Theoretical Pre-Image: {theoretical_pre_image}')
    print(f'Actual Pre-Image:      {pre_image_y_plots}')
    print(f'Bit Lengths:           {bit_lengths}\n')

    print("Done!")

