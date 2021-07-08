
// stub for developing on a platform with no sensor installed

struct RTIMUSettings
{
  RTIMUSettings(const char*) {}

};

inline const int RTIMU_TYPE_NULL = 0;

struct RTIMU_DATA
{
  double pressure = 0.0;
  double temperature = -273.15;
  double humidity = -1.0;
};

struct RTIMU
{
  static RTIMU* createIMU(const RTIMUSettings*) { return new RTIMU;}
  bool IMUInit() const { return true; }
  int IMUType() const { return 1; }
  void setSlerpPower(double) { }
  void setGyroEnable(bool) { }
  void setAccelEnable(bool) { }
  void setCompassEnable(bool) { }
  int IMUGetPollInterval() { return 0; }
  bool IMURead() { return true; }
  RTIMU_DATA getIMUData() { return RTIMU_DATA(); }
};

struct RTPressure
{
  static RTPressure* createPressure(const RTIMUSettings*) { return new RTPressure;}
  bool pressureInit() const { return true; }
  void pressureRead(RTIMU_DATA&) const {}
};

struct RTHumidity
{
  static RTHumidity* createHumidity(const RTIMUSettings*) { return new RTHumidity;}
  bool humidityInit() const { return true; }
  void humidityRead(RTIMU_DATA&) const {}
};