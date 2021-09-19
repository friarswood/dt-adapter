#pragma once

// stubbed UART serial functions

inline int serialOpen(const std::string&, int)
{
  return 0;
}

// this doesn't get called
inline ssize_t read(int, byte* bytes, size_t len)
{
  // ramp up from 400 to 655 then back to 400
  static byte counter = 0;
  bytes[2] = byte((400 + counter) >> 8);
  bytes[3] = byte((400 + counter) & 0xff);
  ++counter;
  return len;
}

inline ssize_t write(int, const byte*, size_t len)
{
  return len;
}