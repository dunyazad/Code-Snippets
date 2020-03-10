#pragma once

#include <string>
#define _CRT_SECURE_NO_WARNINGS

class Console
{
	static Console* sConsole;

	static std::string log;

	Console() {}

public:
	static void initialize(int posX, int posY, int verticalSize)
	{
		if( sConsole == NULL )
		{
			AllocConsole();
			freopen( "CONOUT$", "wt", stdout );
			HWND ConsolehWnd = GetConsoleWindow();

			SetWindowPos( ConsolehWnd, HWND_TOPMOST,                          
				posX, posY, 800, verticalSize, SWP_SHOWWINDOW );

			sConsole = new Console();
		}
	}

	static void terminate()
	{
		delete sConsole;
		sConsole = NULL;

		FreeConsole();
	}

	static void OutLog(char *str, ...)
	{
		char msg[1024];

		va_list va;
		va_start(va, str);

		vsprintf(msg, str, va);

		va_end(va) ;
		printf("%s", msg);

		//log.append(msg);
	}

	static void OutLogString(char *str, ...)
	{
		char msg[1024];

		va_list va;
		va_start(va, str);

		vsprintf(msg, str, va);

		va_end(va) ;
		printf("%s\n", msg);

		//log.append(msg);
	}

	/*void flush()
	{
		FILE* fp = OpenFile(
	}*/
};

Console* Console::sConsole = 0;