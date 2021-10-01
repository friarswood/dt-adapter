#pragma once

#include <chrono>
#include <ctime>

inline const char* utc_now()
{
  time_t tt = std::chrono::system_clock::to_time_t(std::chrono::system_clock::now());
  struct tm* ttt;
  ttt = gmtime(&tt);
  static char buffer[32];
  strftime(buffer, sizeof(buffer), "%Y-%m-%dT%H:%M:%SZ", ttt);
  return buffer;
}

