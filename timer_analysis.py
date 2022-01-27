import json
from statistics import mean,stdev
import numpy as np
import matplotlib.pyplot as plt

with open('encrypted_timer.json') as f:
    encrypted_timer=json.load(f)
with open('decrypted_timer.json') as f:
    decrypted_timer=json.load(f)
with open('diffie_hellman_timer.json') as f:
    diffie_hellman_timer=json.load(f)


print("Encrypted timer(Maximum):",max(encrypted_timer),
	"\nEncrypted timer(Minimum):",min(encrypted_timer),
	"\nEncrypted timer(Mean):",mean(encrypted_timer),
	"\nEncrypted timer(Stdev):",stdev(encrypted_timer))

print("\n\nDecrypted timer(Maximum):",max(decrypted_timer),
	"\nDecrypted timer(Minimum):",min(decrypted_timer),
	"\nDecrypted timer(Mean):",mean(decrypted_timer),
	"\nDecrypted timer(Stdev):",stdev(decrypted_timer))

print("\n\nDiffie Hellman timer(Maximum):",max(diffie_hellman_timer),
	"\nDiffie Hellman timer(Minimum):",min(diffie_hellman_timer),
	"\nDiffie Hellman timer(Mean):",mean(diffie_hellman_timer),
	"\nDiffie Hellman timer(Stdev):",stdev(diffie_hellman_timer))

EncryptedTimer=[max(encrypted_timer),min(encrypted_timer),mean(encrypted_timer),stdev(encrypted_timer)]
DecryptedTimer=[max(decrypted_timer),min(decrypted_timer),mean(decrypted_timer),stdev(decrypted_timer)]
DiffieHellmanTimer=[max(diffie_hellman_timer),min(diffie_hellman_timer),mean(diffie_hellman_timer),stdev(diffie_hellman_timer)]

barWidth = 0.25
fig = plt.subplots(figsize =(12, 8))

br1 = np.arange(len(EncryptedTimer))
br2 = [x + barWidth for x in br1]
br3 = [x + barWidth for x in br2]

plt.bar(br1, EncryptedTimer, color ='r', width = barWidth,
        edgecolor ='grey', label ='Encrypted Timer')
plt.bar(br2, DecryptedTimer, color ='g', width = barWidth,
        edgecolor ='grey', label ='Decrypted Timer')
plt.bar(br3, DiffieHellmanTimer, color ='b', width = barWidth,
        edgecolor ='grey', label ='Diffie Hellman Timer')

plt.xlabel('Metric', fontweight ='bold', fontsize = 15)
plt.ylabel('Time(s)', fontweight ='bold', fontsize = 15)
plt.xticks([r + barWidth for r in range(len(EncryptedTimer))],
		   ['Maximum', 'Minimum', 'Mean', 'Standard Deviation'])
 
plt.legend()
plt.show()

