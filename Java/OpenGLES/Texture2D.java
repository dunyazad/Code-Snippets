package com.imc;

import android.content.Context;
import android.content.res.AssetManager;
import android.opengl.GLES20;

import java.io.IOException;
import java.io.InputStream;
import java.nio.ByteBuffer;
import java.nio.ByteOrder;
import java.nio.FloatBuffer;
import java.nio.ShortBuffer;
import java.nio.charset.StandardCharsets;

public class Texture2D {
    private static final String TAG = Texture2D.class.getSimpleName();

    private static final float SQUARE_COORDS[] = {
            -1f, 1f, 0.0f,
            -1f, -1f, 0.0f,
            1f, -1f, 0.0f,
            1f, 1f, 0.0f
    };

    private static final float UVS[] = {
            0.0f, 0.0f, // Top Left (V2)
            0.0f, 1.0f, // Bottom Left (V1)
            1.0f, 1.0f, // Top Right (V4)
            1.0f, 0.0f  // Bottom Right (V3)
    };

    protected static final short DRAW_ORDER[] = {0, 1, 2, 0, 2, 3};
    protected static final int COORDS_PER_VERTEX = 3;
    protected static final int VERTEX_STRIDE = COORDS_PER_VERTEX * 4;

    protected Context mContext;

    protected ShortBuffer mDrawListBuffer;
    protected FloatBuffer mVertexBuffer;
    protected FloatBuffer mUVBuffer;

    protected String mVertexCode_mono;
    protected String mVertexCode_left;
    protected String mVertexCode_right;
    protected String mFragmentCode;

    protected int mTextureID;
    protected int mProgram_mono;
    protected int mProgram_left;
    protected int mProgram_right;
    protected int mTextureWidth;
    protected int mTextureHeight;

    public Texture2D(Context context, int textureWidth, int textureHeight) {
        mContext = context;
        mTextureWidth = textureWidth;
        mTextureHeight = textureHeight;
    }

    public void initialize() {
        initializeVertex();
        initializeShader();
        createProgram();

        int[] textureIDs = new int[1];
        GLES20.glGenTextures(1, textureIDs, 0);
        mTextureID = textureIDs[0];
        GLES20.glBindTexture(GLES20.GL_TEXTURE_2D, mTextureID);

        GLES20.glTexParameterf(GLES20.GL_TEXTURE_2D, GLES20.GL_TEXTURE_MIN_FILTER, GLES20.GL_NEAREST);
        GLES20.glTexParameterf(GLES20.GL_TEXTURE_2D, GLES20.GL_TEXTURE_MAG_FILTER, GLES20.GL_LINEAR);

        GLES20.glTexParameteri(GLES20.GL_TEXTURE_2D, GLES20.GL_TEXTURE_WRAP_S, GLES20.GL_CLAMP_TO_EDGE);
        GLES20.glTexParameteri(GLES20.GL_TEXTURE_2D, GLES20.GL_TEXTURE_WRAP_T, GLES20.GL_CLAMP_TO_EDGE);

        GLES20.glTexImage2D(GLES20.GL_TEXTURE_2D, 0, GLES20.GL_RGBA, mTextureWidth, mTextureHeight, 0, GLES20.GL_RGBA, GLES20.GL_UNSIGNED_BYTE, null);
        GLES20.glBindTexture(GLES20.GL_TEXTURE_2D, 0);
    }

    protected void initializeVertex() {
        ByteBuffer vertexBuffer = ByteBuffer.allocateDirect(SQUARE_COORDS.length * 4);
        vertexBuffer.order(ByteOrder.nativeOrder());

        mVertexBuffer = vertexBuffer.asFloatBuffer();
        mVertexBuffer.put(SQUARE_COORDS);
        mVertexBuffer.position(0);

        ByteBuffer drawListBuffer = ByteBuffer.allocateDirect(DRAW_ORDER.length * 2);
        drawListBuffer.order(ByteOrder.nativeOrder());

        mDrawListBuffer = drawListBuffer.asShortBuffer();
        mDrawListBuffer.put(DRAW_ORDER);
        mDrawListBuffer.position(0);

        ByteBuffer uvBuffer = ByteBuffer.allocateDirect(UVS.length * 4);
        uvBuffer.order(ByteOrder.nativeOrder());
        mUVBuffer = uvBuffer.asFloatBuffer();
        mUVBuffer.put(UVS);
        mUVBuffer.position(0);
    }

    protected void initializeShader() {
        mVertexCode_mono = readShader("vertex.glsl");
        mVertexCode_left = readShader("vertex_left.glsl");
        mVertexCode_right = readShader("vertex_right.glsl");
        mFragmentCode = readShader("fragment_default.glsl");
    }

    protected String readShader(String shaderFileName) {
        AssetManager assetManager = mContext.getAssets();
        try {
            InputStream inputStream = assetManager.open(shaderFileName);

            byte[] bytes = new byte[inputStream.available()];
            inputStream.read(bytes, 0, inputStream.available());

            return new String(bytes, StandardCharsets.UTF_8);
        } catch (IOException e) {
            e.printStackTrace();
        }
        return null;
    }

    protected void createProgram() {
        {
            int vertexShader = GLESUtility.loadShader(GLES20.GL_VERTEX_SHADER, mVertexCode_mono);
            int fragmentShader = GLESUtility.loadShader(GLES20.GL_FRAGMENT_SHADER, mFragmentCode);

            mProgram_mono = GLES20.glCreateProgram();
            GLES20.glAttachShader(mProgram_mono, vertexShader);
            GLES20.glAttachShader(mProgram_mono, fragmentShader);
            GLES20.glLinkProgram(mProgram_mono);
        }
        {
            int vertexShader = GLESUtility.loadShader(GLES20.GL_VERTEX_SHADER, mVertexCode_left);
            int fragmentShader = GLESUtility.loadShader(GLES20.GL_FRAGMENT_SHADER, mFragmentCode);

            mProgram_left = GLES20.glCreateProgram();
            GLES20.glAttachShader(mProgram_left, vertexShader);
            GLES20.glAttachShader(mProgram_left, fragmentShader);
            GLES20.glLinkProgram(mProgram_left);
        }
        {
            int vertexShader = GLESUtility.loadShader(GLES20.GL_VERTEX_SHADER, mVertexCode_right);
            int fragmentShader = GLESUtility.loadShader(GLES20.GL_FRAGMENT_SHADER, mFragmentCode);

            mProgram_right = GLES20.glCreateProgram();
            GLES20.glAttachShader(mProgram_right, vertexShader);
            GLES20.glAttachShader(mProgram_right, fragmentShader);
            GLES20.glLinkProgram(mProgram_right);
        }
    }

    public int getTextureID() {
        return mTextureID;
    }

    public int getTextureWidth() {
        return mTextureWidth;
    }

    public int getTextureHeight() {
        return mTextureHeight;
    }

    public void destroy() {
        if (mTextureID != 0) {
            int[] textureId = new int[1];
            textureId[0] = mTextureID;
            GLES20.glDeleteTextures(1, textureId, 0);
            mTextureID = 0;
        }
    }
}
