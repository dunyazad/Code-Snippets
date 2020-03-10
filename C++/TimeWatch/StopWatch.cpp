#include "StopWatch.h"
#include <iostream>
using namespace std;

StopWatchElement::StopWatchElement()
{
}

StopWatchElement::~StopWatchElement()
{
	m_times.clear();
}

void StopWatchElement::Start()
{
	m_times.push_back(chrono::system_clock::now());
}

pair<float, float> StopWatchElement::Touch()
{
	m_times.push_back(chrono::system_clock::now());
	m_fromBegin = m_times[m_times.size() - 1] - m_times[0];
	m_fromLast = m_times[m_times.size() - 1] - m_times[m_times.size() - 2];
	float fromBegin = float(std::chrono::duration_cast<std::chrono::milliseconds>(m_fromBegin).count()) / 1000;
	float fromLast = float(std::chrono::duration_cast<std::chrono::milliseconds>(m_fromLast).count()) / 1000;
	return make_pair(fromBegin, fromLast);
}

pair<float, float> StopWatchElement::Stop()
{
	m_times.push_back(chrono::system_clock::now());
	m_fromBegin = m_times[m_times.size() - 1] - m_times[0];
	m_fromLast = m_times[m_times.size() - 1] - m_times[m_times.size() - 2];
	float fromBegin = float(std::chrono::duration_cast<std::chrono::milliseconds>(m_fromBegin).count()) / 1000;
	float fromLast = float(std::chrono::duration_cast<std::chrono::milliseconds>(m_fromLast).count()) / 1000;
	cout << fromBegin << " from beginning" << endl;
	cout << fromLast << " from last" << endl;
	return make_pair(fromBegin, fromLast);
}

void StopWatchElement::Reset()
{
	m_times.clear();
}

StopWatch StopWatch::s_instance;
map<string, StopWatchElement*> StopWatch::s_stopwatches;

StopWatch::StopWatch()
{
}

StopWatch::~StopWatch()
{
}

StopWatchElement* StopWatch::GetStopWatch(const string& key)
{
	if (s_stopwatches.count(key) == 0)
	{
		return nullptr;
	}
	else
	{
		return s_stopwatches[key];
	}
}

StopWatchElement* StopWatch::SetStopWatch(const string& key, StopWatchElement* pStopWatch)
{
	if (s_stopwatches.count(key) != 0)
	{
		delete s_stopwatches[key];
	}

	s_stopwatches[key] = pStopWatch;
	return pStopWatch;
}

void StopWatch::Start(const string& key)
{
	auto pStopWatch = GetStopWatch(key);

	if (pStopWatch == nullptr) {
		pStopWatch = SetStopWatch(key, new StopWatchElement);
	}

	pStopWatch->Start();
}

pair<float, float> StopWatch::Touch(const string& key)
{
	auto pStopWatch = GetStopWatch(key);

	if (pStopWatch == nullptr) {
		pStopWatch = SetStopWatch(key, new StopWatchElement);
		pStopWatch->Start();
	}
	
	return pStopWatch->Touch();
}

pair<float, float> StopWatch::Stop(const string& key)
{
	auto pStopWatch = GetStopWatch(key);

	if (pStopWatch == nullptr) {
		pStopWatch = SetStopWatch(key, new StopWatchElement);
		pStopWatch->Start();
	}

	return pStopWatch->Stop();
}

void StopWatch::Reset(const string& key)
{
	auto pStopWatch = GetStopWatch(key);

	if (pStopWatch == nullptr) {
		pStopWatch = SetStopWatch(key, new StopWatchElement);
		pStopWatch->Start();
	}

	pStopWatch->Reset();
}
