#include "hios.h"
#include "qobject.h"
#include "HSplashDialog.h"
#include <qdir.h>
#include <qmessagebox.h>
#ifndef QT_NO_OPENGL
#include "HGLRender.h"
#endif
#include <QSurfaceFormat>
#include <QtWidgets/QApplication>
#include "DeviceData.h"
#include "logutils.h"
#include <qresource.h>

#include <QSharedMemory>  

#include "HDeviceManager.h"
#include "HMessageBox.h"

#include "HMemoryDebug.h" // 메모리 릭 체크용

#include <windows.h>
#include <DbgHelp.h>
#include <tchar.h>
#pragma comment (lib, "DbgHelp.lib")

#ifdef _DEBUG
#pragma comment(linker, "/entry:WinMainCRTStartup /subsystem:console")
#endif

LONG WINAPI UnhandledExceptionFilterC(EXCEPTION_POINTERS* ExceptionInfo);

void CreateMiniDump(EXCEPTION_POINTERS* pep)
{
    // Create a dump file
    HANDLE hFile = CreateFile(_T("crash_dump.dmp"), GENERIC_READ | GENERIC_WRITE,
        0, nullptr, CREATE_ALWAYS, FILE_ATTRIBUTE_NORMAL, nullptr);

    if ((hFile != nullptr) && (hFile != INVALID_HANDLE_VALUE))
    {
        // Create the minidump
        MINIDUMP_EXCEPTION_INFORMATION mdei;
        mdei.ThreadId = GetCurrentThreadId();
        mdei.ExceptionPointers = pep;
        mdei.ClientPointers = FALSE;

        MINIDUMP_TYPE mdt = (MINIDUMP_TYPE)(MiniDumpWithPrivateReadWriteMemory |
            MiniDumpWithDataSegs |
            MiniDumpWithHandleData |
            MiniDumpWithFullMemoryInfo |
            MiniDumpWithThreadInfo |
            MiniDumpWithUnloadedModules);

        MiniDumpWriteDump(GetCurrentProcess(), GetCurrentProcessId(), hFile, mdt, (pep != nullptr) ? &mdei : nullptr, nullptr, nullptr);

        CloseHandle(hFile);
    }
}

int main(int argc, char* argv[])
{
#ifdef _DEBUG
#if defined(_MSC_VER)
    _CrtSetDbgFlag(_CRTDBG_ALLOC_MEM_DF | _CRTDBG_LEAK_CHECK_DF);
    //prevHook = _CrtSetReportHook(customReportHook);
    //_CrtSetBreakAlloc(639); // 여기서 메모리 할당번호를 입력해서 어떤 메모리가 메모리가 해제가 되지 않았는지 파악
#endif
#endif

    SetUnhandledExceptionFilter(UnhandledExceptionFilterC);


    QApplication a(argc, argv);
    QDir dir;
    if (!dir.exists(LOCAL_PATH_LOG))
        dir.mkdir(LOCAL_PATH_LOG);
    LOGUTILS::initLogging(LOCAL_PATH_LOG, "L-Scan");

    a.setWindowIcon(QIcon("icon.ico"));
    QResource::registerResource(qApp->applicationDirPath() + "/animation.qrc");
    qDebug() << qApp->applicationDirPath();

    if (!DEVICE_MANAGER->CheckCudaEnvironment())
    {
        //HMSGBOX->confirm("CUDA device not found");
        QMessageBox kQMBMsg(QMessageBox::Critical, "ERROR", "CUDA device not found.", 0);
        kQMBMsg.exec();
        exit(0);
    }


    QStringList list = a.arguments();//[program_exe] args...
    QString caseID = "";
    QString port = "";
    if (list.size() > 1)
    {
        caseID = list.at(1);
        port = list.at(2);
    }


    QSharedMemory shared("20230302");
    if (!shared.create(512, QSharedMemory::ReadWrite))
    {
        QMessageBox kQMBMsg(QMessageBox::Critical, "Notice", "Same process is already working. Close this process.", 0);
        kQMBMsg.exec();
        exit(0);
    }
    hios* w = new hios();

    HSplashDialog splash;
    QObject::connect(w, &hios::SendSplash, &splash, &HSplashDialog::AddMsg);
    w->InitializeVariable();
    splash.SetVersion(w->GetVersion());
    splash.show();
    splash.activateWindow();
    QApplication::processEvents();
    w->InitializeHIOS();
    w->AfterInitialize(caseID, port);
    splash.close();

    //w.show();
    w->SetFullscreen(true);
    w->setWindowState(w->windowState() & ~Qt::WindowMinimized);
    w->raise();
    w->activateWindow();

    int result = a.exec();

    delete w;
    return result;
}

LONG WINAPI UnhandledExceptionFilterC(EXCEPTION_POINTERS* ExceptionInfo)
{
    CreateMiniDump(ExceptionInfo);
    return EXCEPTION_EXECUTE_HANDLER;
}