import binascii
import hashlib
import os
import random

#**********************************************************************************
#			   Apache License
#         Version 2.0, January 2004
#     Copyright 2015 Amirali Sanatinia
#     Modification: Excess Keys Removed
primes = {
	# 2048-bit
	14: {
	"prime": 0xFFFFFFFFFFFFFFFFC90FDAA22168C234C4C6628B80DC1CD129024E088A67CC74020BBEA63B139B22514A08798E3404DDEF9519B3CD3A431B302B0A6DF25F14374FE1356D6D51C245E485B576625E7EC6F44C42E9A637ED6B0BFF5CB6F406B7EDEE386BFB5A899FA5AE9F24117C4B1FE649286651ECE45B3DC2007CB8A163BF0598DA48361C55D39A69163FA8FD24CF5F83655D23DCA3AD961C62F356208552BB9ED529077096966D670C354E4ABC9804F1746C08CA18217C32905E462E36CE3BE39E772C180E86039B2783A2EC07A28FB5C55DF06F4C52C9DE2BCBF6955817183995497CEA956AE515D2261898FA051015728E5A8AACAA68FFFFFFFFFFFFFFFF,
	"generator": 2
	},
}

class DiffieHellman:
	""" Class to represent the Diffie-Hellman key exchange protocol """
	# Current minimum recommendation is 2048 bit.
	def __init__(self, group=14):
		if group in primes:
			self.p = primes[group]["prime"]
			self.g = primes[group]["generator"]
		else:
			raise Exception("Group not supported")

		self.__a = int(binascii.hexlify(os.urandom(32)), base=16)

	def get_private_key(self):
		""" Return the private key (a) """
		return self.__a

	def gen_public_key(self):
		""" Return A, A = g ^ a mod p """
		# calculate G^a mod p
		return pow(self.g, self.__a, self.p)

	def check_other_public_key(self, other_contribution):
		# check if the other public key is valid based on NIST SP800-56
		# 2 <= g^b <= p-2 and Lagrange for safe primes (g^bq)=1, q=(p-1)/2

		if 2 <= other_contribution and other_contribution <= self.p - 2:
			if pow(other_contribution, (self.p - 1) // 2, self.p) == 1:
				return True
		return False

	def gen_shared_key(self, other_contribution):
		""" Return g ^ ab mod p """
		# calculate the shared key G^ab mod p
		if self.check_other_public_key(other_contribution):
			self.shared_key = pow(other_contribution, self.__a, self.p)
			return hashlib.sha256(str(self.shared_key).encode()).hexdigest()
		else:
			raise Exception("Bad public key from other party")
# ************************************************************************************