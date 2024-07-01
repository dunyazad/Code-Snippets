	{ // 생성 코드
		int cx = 0;			// 중심 좌표 X
		int cy = 0;			// 중심 좌표 Y
		int cz = 0;			// 중심 좌표 Z
		int offset = 3;		// 중심으로 부터의 개수 ex) 3이면 중심 +- 3 이므로 7 x 7 x 7로 동작
		int currentOffset = 0;
		while (currentOffset <= offset)
		{
			for (int z = -currentOffset; z <= currentOffset; z++)
			{
				for (int y = -currentOffset; y <= currentOffset; y++)
				{
					for (int x = -currentOffset; x <= currentOffset; x++)
					{
						if ((x == -currentOffset || x == currentOffset) ||
							(y == -currentOffset || y == currentOffset) ||
							(z == -currentOffset || z == currentOffset))
						{
							printf("%d, %d, %d,\n", cx + x, cy + y, cz + z);
						}
					}
				}
			}
			currentOffset++;
		}
	}
