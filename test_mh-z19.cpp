// g++ -Wall -Werror -std=c++17 mh-z19.cpp -lwiringPi -o test-mh19

#include <wiringPi.h>
#include <wiringSerial.h>  //only needed for serialOpen

#include <array>
#include <iostream>
#include <unistd.h>        // needed for read and write

#include <termios.h>

const size_t MSG_LEN = 9;

typedef unsigned char byte;

const std::array<byte, MSG_LEN> REQUEST_READING{0xFF,0x01,0x86,0x00,0x00,0x00,0x00,0x00,0x79};
const std::array<byte, MSG_LEN> START_CALIBRATION{0xFF,0x01,0x79,0xa0,0x00,0x00,0x00,0x00,0xe6};
const std::array<byte, MSG_LEN> STOP_CALIBRATION{0xFF,0x01,0x79,0x00,0x00,0x00,0x00,0x00,0x86};
const std::array<byte, MSG_LEN> SETRANGE2000{0xFF, 0x01, 0x99, 0x00, 0x00, 0x00, byte(2000 >> 8), byte(2000 / 256), 0x00};
const std::array<byte, MSG_LEN> SETRANGE5000{0xFF, 0x01, 0x99, 0x00, 0x00, 0x00, byte(5000 >> 8), byte(5000 / 256), 0x00};

byte checksum(const byte* const msg)
{
  char checksum = 0;
  for(size_t i = 1; i < MSG_LEN-1; ++i)
  {
    checksum += msg[i];
  }
  checksum = 0xff - checksum;
  return checksum + 1;
}

bool validate(const byte* msg)
{
  //std::cout << (int)checksum(msg) << "==" << (int)msg[MSG_LEN-1] << std::endl;
  return checksum(msg) == msg[MSG_LEN-1];
}

void print(const byte* msg, int len=MSG_LEN)
{
  for (size_t i = 0; i < MSG_LEN; ++i)
    std::cout << std::hex << (int)msg[i] << " ";
  std::cout << "[" << validate(msg) << "]" << std::endl;
}

int main()
{
  int wait = 1000;   // ms
  int fd = serialOpen("/dev/serial0", 9600);
  if (fd < 0)
  {
    std::cerr << "Unable to open device";
    return 1;
  }

  termios options;
  tcgetattr(fd, &options);   // Read current options
  options.c_cflag |= CS7;
  tcsetattr(fd, 0, &options);   // Read current options

  // std::cout << std::hex << (int)checksum(REQUEST_READING) << std::endl;
  // std::cout << std::hex << (int)checksum(START_CALIBRATION) << std::endl;
  // std::cout << std::hex << (int)checksum(STOP_CALIBRATION) << std::endl;
  std::cout << "ttyAMA0 initialised [ok]" << std::endl;
  std::array<byte, MSG_LEN> response{};
  std::cout << write(fd, SETRANGE2000.data(), SETRANGE2000.size()) << std::endl;
  delay(wait);
  for (;;)
  {
    print(REQUEST_READING.data());
    std::cout << write(fd, REQUEST_READING.data(), REQUEST_READING.size()) << std::endl;
    //delay(wait);
    std::cout << read(fd, response.data(), response.size()) << std::endl;
    print(response.data());
    delay(wait);
  }
}
