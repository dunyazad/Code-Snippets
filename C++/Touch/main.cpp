#include <stdio.h>

int main(int argc, char** argv)
{
	if (argc < 2)
	{
		printf("Please enter file name.\n");

		return 1;
	}

	FILE* fp = nullptr;
	auto err = fopen_s(&fp, argv[1], "r");

	if (err == 0)
	{
		printf("File exists.\n");

		return 1;
	}
	else
	{
		err = fopen_s(&fp, argv[1], "w");
	}

	fclose(fp);

	return 0;
}
