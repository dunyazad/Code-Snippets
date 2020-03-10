package com.imc;

import android.opengl.EGL14;
import android.opengl.EGLConfig;
import android.opengl.EGLContext;
import android.opengl.EGLDisplay;
import android.opengl.EGLSurface;
import android.util.Log;

public class SurfaceManager {
    private EGLContext mEGLSharedContext;
    private EGLContext mEGLContext;
    private EGLDisplay mEGLDisplay;
    private EGLSurface mEGLSurface;

    private EGLContext mSavedEGLContext;
    private EGLDisplay mSavedEGLDisplay;
    private EGLSurface mSavedEGLDrawSurface;
    private EGLSurface mSavedEGLReadSurface;

    public SurfaceManager() {
        mEGLSharedContext = EGL14.eglGetCurrentContext();
        eglSetup();
    }

    public void makeCurrent() {
        EGL14.eglMakeCurrent(mEGLDisplay, mEGLSurface, mEGLSurface, mEGLContext);
        checkEglError("eglMakeCurrent");
    }

    private void eglSetup() {
        mEGLDisplay = EGL14.eglGetDisplay(EGL14.EGL_DEFAULT_DISPLAY);
        checkEglError("eglGetDisplay");

        int[] version = new int[2];
        EGL14.eglInitialize(mEGLDisplay, version, 0, version, 1);
        checkEglError("eglInitialize");

        int[] attribList;
        attribList = new int[]{
                EGL14.EGL_RED_SIZE, 8,
                EGL14.EGL_GREEN_SIZE, 8,
                EGL14.EGL_BLUE_SIZE, 8,
                EGL14.EGL_RENDERABLE_TYPE, EGL14.EGL_OPENGL_ES2_BIT,
                EGL14.EGL_NONE
        };
        EGLConfig[] configs = new EGLConfig[1];
        int[] numConfigs = new int[1];

        EGL14.eglChooseConfig(mEGLDisplay, attribList, 0, configs, 0, configs.length, numConfigs, 0);
        checkEglError("eglChooseConfig");

        int[] attrib_list = {
                EGL14.EGL_CONTEXT_CLIENT_VERSION, 2,
                EGL14.EGL_NONE
        };

        mEGLContext = EGL14.eglCreateContext(mEGLDisplay, configs[0], mEGLSharedContext, attrib_list, 0);
        checkEglError("eglCreateContext");

        int[] surfaceAttribs = {
                EGL14.EGL_NONE
        };
        mEGLSurface = EGL14.eglCreatePbufferSurface(mEGLDisplay, configs[0], surfaceAttribs, 0);
        checkEglError("eglCreatePbufferSurface");
    }

    public void release() {
        if (mEGLDisplay != EGL14.EGL_NO_DISPLAY) {
            EGL14.eglMakeCurrent(mEGLDisplay, EGL14.EGL_NO_SURFACE, EGL14.EGL_NO_SURFACE,
                    EGL14.EGL_NO_CONTEXT);
            EGL14.eglDestroySurface(mEGLDisplay, mEGLSurface);
            EGL14.eglDestroyContext(mEGLDisplay, mEGLContext);
            EGL14.eglReleaseThread();
            EGL14.eglTerminate(mEGLDisplay);
        }
        mEGLSurface = EGL14.EGL_NO_SURFACE;
        mEGLDisplay = EGL14.EGL_NO_DISPLAY;
        mEGLContext = EGL14.EGL_NO_CONTEXT;
    }

    private void checkEglError(String msg) {
        int error;
        if ((error = EGL14.eglGetError()) != EGL14.EGL_SUCCESS) {
            Log.d("Surface2UnityDebug", msg + ": EGL error: 0x" + Integer.toHexString(error));
            throw new RuntimeException(msg + ": EGL error: 0x" + Integer.toHexString(error));
        }
    }

    public void saveRenderState() {
        mSavedEGLDisplay = EGL14.eglGetCurrentDisplay();
        mSavedEGLDrawSurface = EGL14.eglGetCurrentSurface(EGL14.EGL_DRAW);
        mSavedEGLReadSurface = EGL14.eglGetCurrentSurface(EGL14.EGL_READ);
        mSavedEGLContext = EGL14.eglGetCurrentContext();
    }

    public void restoreRenderState() {
        EGL14.eglMakeCurrent(mSavedEGLDisplay, mSavedEGLDrawSurface, mSavedEGLReadSurface, mSavedEGLContext);
    }
}
