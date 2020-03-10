#pragma once

#include <chrono>
using namespace std::chrono;

#include <map>
#include <string>
#include <vector>
using namespace std;

class StopWatchElement
{
public:
	StopWatchElement();
	~StopWatchElement();

	void Start();
	pair<float, float> Touch();
	pair<float, float> Stop();
	void Reset();

private:
	vector<system_clock::time_point> m_times;
	duration<double> m_fromBegin;
	duration<double> m_fromLast;
};

class StopWatch
{
private:
	static StopWatch s_instance;
	static map<string, StopWatchElement*> s_stopwatches;

	StopWatch();
	~StopWatch();

	static StopWatchElement* GetStopWatch(const string& key);
	static StopWatchElement* SetStopWatch(const string& key, StopWatchElement* pStopWatch);

public:
	static void Start(const string& key);
	static pair<float, float> Touch(const string& key);
	static pair<float, float> Stop(const string& key);
	static void Reset(const string& key);
};
