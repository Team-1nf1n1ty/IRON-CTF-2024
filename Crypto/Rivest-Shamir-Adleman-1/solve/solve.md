# Rivest, Shamir, Adleman 1

In this challenge we can notice from the script that first 824 bits of the secret key is revealed. Only 200 bits of secret key is unknown.

This is classic coppersmith attack, I have implemented the solve using the following journal.

Also once we factor the message, if we notice we can't calculate d as gcd(e,phi) != 1.
So we can calculate only c_ = m^3 mod N. 

But analyzing c_ we notice that c_ << N. This may indicate that message was very small that m^3 didn't exceed N(may also be false positive sometimes). So calculating cubroot gives us the flag.

[Gabrielle de Micheli, Nadia Heninger. Recovering cryptographic keys from partial information, by
example. 2020. ￿hal-03045663￿](https://hal.science/hal-03045663/document)

