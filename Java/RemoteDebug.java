package com.imc;

import android.util.Pair;

import java.io.IOException;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
import java.net.SocketException;
import java.net.UnknownHostException;
import java.util.Calendar;
import java.util.HashMap;
import java.util.LinkedList;
import java.util.Queue;
import java.util.concurrent.SynchronousQueue;

public class RemoteDebug {
    static RemoteDebug sInstance = null;
    static String sIP = "192.168.3.121";
    static int sPORT = 7777;
    static InetAddress sServerAddr = null;

    static DatagramSocket sSocket;
    static LinkedList<Pair<String, String>> sMessageQueue = new LinkedList<>();
    static String sCategory = "";
    static String sKey = "";
    static private boolean sWorking = true;

    static HashMap<String, Integer> sMessageCount = new HashMap<String, Integer>();

    public RemoteDebug() {
        new Thread() {
            public void run() {
                try {
                    sSocket = new DatagramSocket();
                    sServerAddr = InetAddress.getByName(sIP);
                } catch (SocketException e) {
                    e.printStackTrace();
                } catch (UnknownHostException e) {
                    e.printStackTrace();
                }

                while(sWorking) {
                    LinkedList<Pair<String, String>> messageQueue = null;
                    synchronized (sMessageQueue) {
                        if(sMessageQueue.size() > 0) {
                            messageQueue = new LinkedList<>(sMessageQueue);
                            sMessageQueue.clear();
                        }
                    }
                    if(messageQueue == null) {
                        try {
                            Thread.sleep(100);
                        } catch (InterruptedException e) {
                            e.printStackTrace();
                        }
                    } else {
                        while(messageQueue.size() != 0) {
                            Pair<String, String> messagePair = messageQueue.getFirst();
                            messageQueue.removeFirst();

                            if (messagePair.first.isEmpty() == false) {
                                String text = "{\"category\" : \"" + sCategory + "\", \"key\" : \"" + sKey + "\", \"date\" : " + messagePair.second + ", \"message\" : \"" + messagePair.first + "\"}";
                                byte[] buf = text.getBytes();
                                DatagramPacket packet = new DatagramPacket(buf, buf.length, sServerAddr, sPORT);

                                try {
                                    sSocket.send(packet);
                                } catch (IOException e) {
                                    e.printStackTrace();
                                }
                            }
                        }
                    }
                }
            }
        }.start();
    }

    static String DateToJSONString() {
        Calendar currentDate = Calendar.getInstance();

        return String.format("{\"year\": \"%4d\", \"month\": \"%2d\", \"day\": \"%2d\", \"hour\": \"%2d\", \"minute\": \"%2d\", \"second\": \"%2d\", \"milisecond\": \"%3d\"}",
                currentDate.get(Calendar.YEAR),
                currentDate.get(Calendar.MONTH),
                currentDate.get(Calendar.DAY_OF_MONTH),
                currentDate.get(Calendar.HOUR),
                currentDate.get(Calendar.MINUTE),
                currentDate.get(Calendar.SECOND),
                currentDate.get(Calendar.MILLISECOND));
    }

    public static void SetMessage(String category, String key, String message) {
            String countKey = category + "." + key;
            if(sMessageCount.containsKey(countKey) == false) {
                sMessageCount.put(countKey, 1);
            } else {
                int count = sMessageCount.get(countKey);
                sMessageCount.put(countKey, count + 1);
            }
            if(message.isEmpty()) {
                synchronized (sMessageQueue) {
                    sMessageQueue.addLast(new Pair<String, String>(String.format("%d", sMessageCount.get(countKey)), DateToJSONString()));
                }
            } else {
                sMessageQueue.addLast(new Pair<String, String> (message, DateToJSONString()));
            }
            if(category.isEmpty()) sCategory = "default"; else sCategory = category;
            if(sKey.isEmpty()) sKey = "default"; else sKey = key;
    }

    public static void Log(String category, String key, String message) {
        if(sInstance == null) {
            sInstance = new RemoteDebug();
        }

        SetMessage(category, key, message);
    }

    public static void Log(String message) {
        if(sInstance == null) {
            sInstance = new RemoteDebug();
        }

        SetMessage("default", "default", message);
    }
}
