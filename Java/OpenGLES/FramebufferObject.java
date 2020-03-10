package com.imc;

import android.opengl.GLES20;

public class FramebufferObject {

    private int mFramebufferObjectID;

    public FramebufferObject(Texture2D texture2D) {
        int[] textureIDs = new int[1];
        GLES20.glGenTextures(1, textureIDs, 0);
        int renderbufferObjectID = textureIDs[0];
        GLES20.glBindTexture(GLES20.GL_TEXTURE_2D, renderbufferObjectID);

        GLES20.glTexImage2D(GLES20.GL_TEXTURE_2D, 0, GLES20.GL_DEPTH_COMPONENT, texture2D.getTextureWidth(), texture2D.getTextureHeight(), 0, GLES20.GL_DEPTH_COMPONENT, GLES20.GL_UNSIGNED_SHORT, null);

        GLES20.glTexParameterf(GLES20.GL_TEXTURE_2D, GLES20.GL_TEXTURE_MIN_FILTER, GLES20.GL_NEAREST);
        GLES20.glTexParameterf(GLES20.GL_TEXTURE_2D, GLES20.GL_TEXTURE_MAG_FILTER, GLES20.GL_LINEAR);

        GLES20.glTexParameteri(GLES20.GL_TEXTURE_2D, GLES20.GL_TEXTURE_WRAP_S, GLES20.GL_CLAMP_TO_EDGE);
        GLES20.glTexParameteri(GLES20.GL_TEXTURE_2D, GLES20.GL_TEXTURE_WRAP_T, GLES20.GL_CLAMP_TO_EDGE);

        GLES20.glBindTexture(GLES20.GL_TEXTURE_2D, 0);

        GLES20.glGenFramebuffers(1, textureIDs, 0);
        mFramebufferObjectID = textureIDs[0];
        GLES20.glBindFramebuffer(GLES20.GL_FRAMEBUFFER, mFramebufferObjectID);
        GLES20.glFramebufferTexture2D(GLES20.GL_FRAMEBUFFER, GLES20.GL_COLOR_ATTACHMENT0, GLES20.GL_TEXTURE_2D, texture2D.getTextureID(), 0);
        GLES20.glFramebufferTexture2D(GLES20.GL_FRAMEBUFFER, GLES20.GL_DEPTH_ATTACHMENT, GLES20.GL_TEXTURE_2D, renderbufferObjectID, 0);

        GLES20.glBindFramebuffer(GLES20.GL_FRAMEBUFFER, 0);
    }

    public void begin() {
        GLES20.glBindFramebuffer(GLES20.GL_FRAMEBUFFER, mFramebufferObjectID);
        GLES20.glBindBuffer(GLES20.GL_ELEMENT_ARRAY_BUFFER, 0);
        GLES20.glBindBuffer(GLES20.GL_ARRAY_BUFFER, 0);
    }

    public void end() {
        GLES20.glBindFramebuffer(GLES20.GL_FRAMEBUFFER, 0);
    }
}
