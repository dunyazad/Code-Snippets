package com.imc;

import android.content.Context;
import android.opengl.GLES11Ext;
import android.opengl.GLES20;

public class Texture2DExtension extends Texture2D {
    public Texture2DExtension(Context context, int textureWidth, int textureHeight) {
        super(context, textureWidth, textureHeight);
    }

    public enum DrawType {Mono, LeftEye, RightEye}

    ;

    @Override
    public void initialize() {
        initializeVertex();
        initializeShader();
        createProgram();

        int[] textureIDs = new int[1];
        GLES20.glGenTextures(1, textureIDs, 0);
        mTextureID = textureIDs[0];
        GLES20.glBindTexture(GLES11Ext.GL_TEXTURE_EXTERNAL_OES, mTextureID);

        GLES20.glTexParameterf(GLES11Ext.GL_TEXTURE_EXTERNAL_OES, GLES20.GL_TEXTURE_MIN_FILTER, GLES20.GL_NEAREST);
        GLES20.glTexParameterf(GLES11Ext.GL_TEXTURE_EXTERNAL_OES, GLES20.GL_TEXTURE_MAG_FILTER, GLES20.GL_LINEAR);

        GLES20.glTexParameteri(GLES20.GL_TEXTURE_2D, GLES20.GL_TEXTURE_WRAP_S, GLES20.GL_CLAMP_TO_EDGE);
        GLES20.glTexParameteri(GLES20.GL_TEXTURE_2D, GLES20.GL_TEXTURE_WRAP_T, GLES20.GL_CLAMP_TO_EDGE);
    }

    @Override
    protected void initializeShader() {
        super.initializeShader();
        mFragmentCode = readShader("fragment_ext.glsl");
    }

    public void draw(DrawType drawType) {
        GLES20.glClearColor(0f, 0f, 0f, 1f);
        GLES20.glClear(GLES20.GL_DEPTH_BUFFER_BIT | GLES20.GL_COLOR_BUFFER_BIT);


        if (drawType == DrawType.Mono) {
            GLES20.glUseProgram(mProgram_mono);

            GLES20.glBindBuffer(GLES20.GL_ELEMENT_ARRAY_BUFFER, 0);
            GLES20.glBindBuffer(GLES20.GL_ARRAY_BUFFER, 0);

            GLES20.glActiveTexture(GLES20.GL_TEXTURE0);
            GLES20.glBindTexture(GLES11Ext.GL_TEXTURE_EXTERNAL_OES, mTextureID);

            int positionHandle = GLES20.glGetAttribLocation(mProgram_mono, "aPosition");
            GLES20.glEnableVertexAttribArray(positionHandle);
            GLES20.glVertexAttribPointer(positionHandle, COORDS_PER_VERTEX, GLES20.GL_FLOAT, false, VERTEX_STRIDE, mVertexBuffer);

            int textureCoordHandle = GLES20.glGetAttribLocation(mProgram_mono, "aTextureCoord");
            GLES20.glVertexAttribPointer(textureCoordHandle, 2, GLES20.GL_FLOAT, false, 0, mUVBuffer);
            GLES20.glEnableVertexAttribArray(textureCoordHandle);

            int textureHandle = GLES20.glGetUniformLocation(mProgram_mono, "sTexture");
            GLES20.glUniform1i(textureHandle, 0);
        } else if (drawType == DrawType.LeftEye) {
            GLES20.glUseProgram(mProgram_left);

            GLES20.glBindBuffer(GLES20.GL_ELEMENT_ARRAY_BUFFER, 0);
            GLES20.glBindBuffer(GLES20.GL_ARRAY_BUFFER, 0);

            GLES20.glActiveTexture(GLES20.GL_TEXTURE0);
            GLES20.glBindTexture(GLES11Ext.GL_TEXTURE_EXTERNAL_OES, mTextureID);

            int positionHandle = GLES20.glGetAttribLocation(mProgram_left, "aPosition");
            GLES20.glEnableVertexAttribArray(positionHandle);
            GLES20.glVertexAttribPointer(positionHandle, COORDS_PER_VERTEX, GLES20.GL_FLOAT, false, VERTEX_STRIDE, mVertexBuffer);

            int textureCoordHandle = GLES20.glGetAttribLocation(mProgram_left, "aTextureCoord");
            GLES20.glVertexAttribPointer(textureCoordHandle, 2, GLES20.GL_FLOAT, false, 0, mUVBuffer);
            GLES20.glEnableVertexAttribArray(textureCoordHandle);

            int textureHandle = GLES20.glGetUniformLocation(mProgram_left, "sTexture");
            GLES20.glUniform1i(textureHandle, 0);
        } else if (drawType == DrawType.RightEye) {
            GLES20.glUseProgram(mProgram_right);

            GLES20.glBindBuffer(GLES20.GL_ELEMENT_ARRAY_BUFFER, 0);
            GLES20.glBindBuffer(GLES20.GL_ARRAY_BUFFER, 0);

            GLES20.glActiveTexture(GLES20.GL_TEXTURE0);
            GLES20.glBindTexture(GLES11Ext.GL_TEXTURE_EXTERNAL_OES, mTextureID);

            int positionHandle = GLES20.glGetAttribLocation(mProgram_right, "aPosition");
            GLES20.glEnableVertexAttribArray(positionHandle);
            GLES20.glVertexAttribPointer(positionHandle, COORDS_PER_VERTEX, GLES20.GL_FLOAT, false, VERTEX_STRIDE, mVertexBuffer);

            int textureCoordHandle = GLES20.glGetAttribLocation(mProgram_right, "aTextureCoord");
            GLES20.glVertexAttribPointer(textureCoordHandle, 2, GLES20.GL_FLOAT, false, 0, mUVBuffer);
            GLES20.glEnableVertexAttribArray(textureCoordHandle);

            int textureHandle = GLES20.glGetUniformLocation(mProgram_right, "sTexture");
            GLES20.glUniform1i(textureHandle, 0);
        }


        GLES20.glDrawElements(GLES20.GL_TRIANGLES, DRAW_ORDER.length, GLES20.GL_UNSIGNED_SHORT, mDrawListBuffer);

        GLES20.glBindTexture(GLES11Ext.GL_TEXTURE_EXTERNAL_OES, 0);
    }
}
