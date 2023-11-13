#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>

// Función para generar un valor aleatorio en un rango específico
float getRandomValue(float min, float max) {
    return ((float)rand() / RAND_MAX) * (max - min) + min;
}

// Función para generar un valor aleatorio entero en un rango específico
int getRandomIntValue(int min, int max) {
    return rand() % (max - min + 1) + min;
}

int main() {
    // Inicializar la semilla para generar valores aleatorios diferentes en cada ejecución
    srand(time(NULL));
    
    // Genera el timestamp
    time_t tiempo_actual = time(NULL);
    
    // Generar valores aleatorios para el sensor THPC
    float Temp = getRandomValue(5.0, 30.0);
    // Redondear Temp a un solo decimal
    Temp = ((int)(Temp * 10)) / 10.0;
    int hum = getRandomIntValue(30, 80);
    int pres = getRandomIntValue(1000, 1200);
    float Co = getRandomValue(30.0, 200.0);
    // Redondear Co a un solo decimal
    Co = ((int)(Co * 10)) / 10.0;

    // Generar valor aleatorio para el sensor Batt
    int BattValue = getRandomIntValue(1, 100);

    // Generar valores aleatorios para el sensor Acelerometer_kpi
    float Amp_x = getRandomValue(0.0059, 0.12);
    // Redondear Amp_x a cuatro decimales
    Amp_x = round(Amp_x * 10000) / 10000.0;
    float Frec_x = getRandomValue(29.0, 31.0);
    // Redondear Frec_x a un solo decimal
    Frec_x = ((int)(Frec_x * 10)) / 10.0;
    float Amp_y = getRandomValue(0.0041, 0.11);
    // Redondear Amp_y a cuatro decimales
    Amp_y = round(Amp_y * 10000) / 10000.0;
    float Frec_y = getRandomValue(59.0, 61.0);
    // Redondear Frec_y a un solo decimal
    Frec_y = ((int)(Frec_y * 10)) / 10.0;
    float Amp_z = getRandomValue(0.008, 0.15);
    // Redondear Amp_z a cuatro decimales
    Amp_z = round(Amp_z * 10000) / 10000.0;
    float Frec_z = getRandomValue(89.0, 91.0);
    // Redondear Frec_z a un solo decimal
    Frec_z = ((int)(Frec_z * 10)) / 10.0;

    // Calcular RMS para Acelerometer_kpi
    float RMS = sqrt(pow(Amp_x, 2) + pow(Amp_y, 2) + pow(Amp_z, 2));
    // Redondear RMS a cuatro decimales
    RMS = round(RMS * 10000) / 10000.0;
    
    // ID Protocol 0
    double ID_Protocol_0[] = {1, BattValue, tiempo_actual};
    
    // ID Protocol 1
    double ID_Protocol_1[] = {1, BattValue, tiempo_actual, Temp, pres, hum, Co};
    
    // ID Protocol 2
    double ID_Protocol_2[] = {1, BattValue, tiempo_actual, Temp, pres, hum, Co, RMS};
    
    // ID Protocol 3
    double ID_Protocol_3[] = {1, BattValue, tiempo_actual, Temp, pres, hum, Co, RMS, Amp_x, Frec_x, Amp_y, Frec_y, Amp_z, Frec_z};
    
    return 0;
}