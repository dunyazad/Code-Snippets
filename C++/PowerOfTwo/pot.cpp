#include <iostream>
#include <bitset>

void printFormattedBinary(int number, int bitWidth = 32) {
	std::bitset<32> binary(number); // 32-bit binary representation of the number
	std::string binaryStr = binary.to_string(); // Convert to string

	// Print the binary string with formatting
	for (int i = 0; i < bitWidth; ++i) {
		std::cout << binaryStr[i];
		if ((i + 1) % 4 == 0 && i != bitWidth - 1) {
			std::cout << " "; // Add a space every 4 bits
		}
	}
	std::cout << std::endl;
}

int main()
{
	int line = 0;
	int n = 17;

	printf("[%3d] n : %d", line++, n); printFormattedBinary(n);

	n--;

	printf("[%3d] n : %d", line++, n); printFormattedBinary(n);
	
	n |= n >> 1;

	printf("[%3d] n : %d", line++, n); printFormattedBinary(n);

	n |= n >> 2;

	printf("[%3d] n : %d", line++, n); printFormattedBinary(n);

	n |= n >> 4;

	printf("[%3d] n : %d", line++, n); printFormattedBinary(n);

	n |= n >> 8;

	printf("[%3d] n : %d", line++, n); printFormattedBinary(n);

	n |= n >> 16;

	printf("[%3d] n : %d", line++, n); printFormattedBinary(n);

	n = n + 1;

	printf("[%3d] n : %d", line++, n); printFormattedBinary(n);

	return 0;
}
