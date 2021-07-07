#pragma once

#include "utils/Global.h"
#include "RTIMULib.h"
#include <string>

class Sensors 
{
public:
  
  struct Status 
  {
    typedef int value;
    static const value OK = 0;
    static const value NO_PRESSURE = 1;
    static const value NO_HUMIDITY = 2;
    static const value NO_IMU = 4;  
  };
  
  Status::value get(std::string& timestamp, double& t, double& p, double& h);
  
  ~Sensors();
  
  Sensors(const Sensors&) = delete;
  Sensors(Sensors&&) = delete;
  Sensors& operator=(const Sensors&) = delete;
  Sensors& operator=(Sensors&&) = delete;

  static std::string statusToString(Sensors::Status::value status);
  
private:

  Sensors();
    
  friend Sensors& Global::instance<Sensors>();

  std::unique_ptr<RTIMUSettings> m_settings;
  std::unique_ptr<RTIMU> m_imu;
  std::unique_ptr<RTPressure> m_pressure;
  std::unique_ptr<RTHumidity> m_humidity;
  Status::value m_status;
};

