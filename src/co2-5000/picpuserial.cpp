// gcc -I/opt/vc/include cpuserial.c -L/opt/vc/lib -lbcm_host -o cpuserial

// based on code here: https://github.com/AndrewFromMelbourne/raspi_serialnumber

#include "picpuserial.h"

#ifdef HAVE_CO2_5000

#include "bcm_host.h"
#include <cstdio>

// assumes that if we have a CO2 sensor, it has no device id and  we are running on a ras pi and use the cpu serial no instread
std::string get_cpu_serialno()
{
  bcm_host_init();

  char response[1024] = {0};

  if (vc_gencmd(response, sizeof(response), "otp_dump") == 0)
  {
    char* saveptr = nullptr;
    char* token = strtok_r(response, "\n", &saveptr);

    while (token != nullptr)
    {
      int index;
      char value[100];

      if (sscanf(token, "%d:%s", &index, value) == 2)
      {
        if (index == 28)
        {
            return value;
        }
      }

      token = strtok_r(nullptr, "\n", &saveptr);
    }
  }

  return "";
}


#else

std::string get_cpu_serialno()
{
  return "testing123";
}

#endif

