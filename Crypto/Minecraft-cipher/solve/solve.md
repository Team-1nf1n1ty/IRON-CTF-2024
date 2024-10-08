# Minecraft cipher

In this challenge we can see that lcg is used to generate a keystream to xor with the bytes of flag.png

Looking next_byte closely, we see that it gives 14 bits of lcg output from 23 bit and rest of the 9 lsb bits and from 24 to 64 all are secret.

Bit of googling will lead you to find truncated lcg. But this version does not give the bytes from msb. Its truncating from the 23 bit. This is essentially like taking mod 2^23.

So we can find a new lcg with mod 2^23. From the known magic bytes of png header, we only have 27 bits of bruteforcing to find the sequential output 9 bits for each output. From which we can find the multiplier and increment value and find the original image.

**Note:** after ctf @kevinychen posted a solution that works efficiently, do check that out https://github.com/kevinychen/flame-ctf-writeups/blob/main/ironCTF-2024/minecraft-cipher.md