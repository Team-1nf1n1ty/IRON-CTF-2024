## Backdoor

The challenge is based on Dual-EC DRBG : https://en.wikipedia.org/wiki/Dual_EC_DRBG
It was found that this pseudo random number generator could have a potential backdoor. Explained very well in this video : https://youtu.be/OkiVN6z60lg?si=MKt4577OB5V-3Ii-

But in the challenge, the backdoor is not directly disclosed. The player has to find it. You may have noticed something is weird with the Elliptic curve parameters. If you try initialize an Elliptic Curve with those parameters, you will probably get an error saying that the given curve is a singular curve. Since discrete log problem on a singular curve is easy to solve, we do that to recover the backdoor.

Once we have the backdoor, we can follow the steps outlined in the video to get the flag. Solve scripts have been attached.