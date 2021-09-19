// g++ -Wall -Werror -std=c++17 mh-z19.cpp -lwiringPi -o test-mh19

#include "mh-z19c.h"

#ifdef HAVE_MH_Z19C
#include <wiringPi.h>
#include <wiringSerial.h>  //only needed for serialOpen
#include <unistd.h> // needed for read and write
#include <termios.h>
#endif

#include <array>

#include <chrono>
#include <ctime>


using namespace std::string_literals;

namespace {

const char* utcStr(const std::chrono::system_clock::time_point t)
{
  time_t tt = std::chrono::system_clock::to_time_t(t);
  struct tm* ttt;
  ttt = gmtime(&tt);
  static char buffer[32];
  strftime(buffer, sizeof(buffer), "%Y-%m-%dT%H:%M:%SZ", ttt);
  return buffer;
}

const std::array<byte, MH_Z19C::MSG_LEN> REQUEST_READING{0xFF,0x01,0x86,0x00,0x00,0x00,0x00,0x00,0x79};
const std::array<byte, MH_Z19C::MSG_LEN> START_CALIBRATION{0xFF,0x01,0x79,0xa0,0x00,0x00,0x00,0x00,0xe6};
const std::array<byte, MH_Z19C::MSG_LEN> STOP_CALIBRATION{0xFF,0x01,0x79,0x00,0x00,0x00,0x00,0x00,0x86};
const std::array<byte, MH_Z19C::MSG_LEN> SETRANGE2000{0xFF, 0x01, 0x99, 0x00, 0x00, 0x00, byte(2000 >> 8), byte(2000 / 256), 0x00};
const std::array<byte, MH_Z19C::MSG_LEN> SETRANGE5000{0xFF, 0x01, 0x99, 0x00, 0x00, 0x00, byte(5000 >> 8), byte(5000 / 256), 0x00};

// byte checksum(const byte* const msg)
// {
//   char checksum = 0;
//   for(size_t i = 1; i < MH_Z19C::MSG_LEN-1; ++i)
//   {
//     checksum += msg[i];
//   }
//   checksum = 0xff - checksum;
//   return checksum + 1;
// }

// bool validate(const byte* msg)
// {
//   //std::cout << (int)checksum(msg) << "==" << (int)msg[MSG_LEN-1] << std::endl;
//   return checksum(msg) == msg[MH_Z19C::MSG_LEN-1];
// }

}


MH_Z19C::MH_Z19C()
  : m_response_buffer{0}
{
#ifdef HAVE_MH_Z19C
  // port is hard-coded...
  m_id = "TODO...";
  m_fd = serialOpen("/dev/serial0", 9600);
#else
  m_id = "testing123";
  m_fd = 0;
#endif
  if (m_fd < 0)
  {
    throw std::runtime_error("Unable to open device");
  }
}

  // termios options;
  // tcgetattr(fd, &options);   // Read current options
  // options.c_cflag |= CS7;
  // tcsetattr(fd, 0, &options);   // Read current options

  // std::cout << std::hex << (int)checksum(REQUEST_READING) << std::endl;
  // std::cout << std::hex << (int)checksum(START_CALIBRATION) << std::endl;
  // std::cout << std::hex << (int)checksum(STOP_CALIBRATION) << std::endl;

py::str MH_Z19C::id() const
{
  return m_id;
}

py::str MH_Z19C::type() const
{
#ifdef HAVE_MH_Z19C
  return "MH-Z19C";
#else
  return "MH-Z19C-STUB";
#endif
}


py::str MH_Z19C::status() const
{
  // TODO
  return "OK";
}

py::dict MH_Z19C::reading()
{
  py::dict result;
  result["status"] = status();
  result["timestamp"] = utcStr(std::chrono::system_clock::now());

#ifdef HAVE_MH_Z19C
  size_t n = write(m_fd, REQUEST_READING.data(), REQUEST_READING.size());
  if (n != MSG_LEN)
  {
    throw std::runtime_error("invalid number of bytes written: "s + std::to_string(n));
  }

  n = read(m_fd, m_response_buffer.data(), m_response_buffer.size());
  if ( != MSG_LEN)
  {
    throw std::runtime_error("invalid number of bytes read: "s + std::to_string(n));
  }
#else
  // ramp up from 400 to 655 then back to 400
  static byte counter = 0;
  m_response_buffer[2] = byte((400 + counter) >> 8);
  m_response_buffer[3] = byte((400 + counter) & 0xff);
  ++counter;
#endif

  result["co2"] = m_response_buffer[2] * 256 +  m_response_buffer[3];

  return result;
}
