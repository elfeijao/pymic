#define FREQ_COLLECT_PRESSURE 50
#define FREQ_COLLECT_FLOW 4

#define SAMPLE_CALIBRATION 1000

#define TIME_COLLECT_FLOW     1000/FREQ_COLLECT_FLOW
#define TIME_COLLECT_PRESSURE 1000/FREQ_COLLECT_PRESSURE

#define PIN_SENSOR_PRESSURE     A0
#define PIN_SENSOR_FLOW         0x02
#define CALIBRATION_FLOW        7
#define LIQUID_DENSITY          1

static float getVoltage();
static float getVolume();
static float getMass();
static void getFrequency();
static void calibrateSensor();

uint16_t frequency;
float calibrate_pressure;
float volumeTotal;
uint64_t  current_time, 
          past_time_pressure, 
          past_time_flow;



// FILTER

#define SIZE_B 5
#define SIZE_A 4

void initialize();
float sum_zeros();
float sum_polos();
void shiftu();
void shifty();

float u[ SIZE_B ];
float y[ SIZE_A + 1 ];

float a[] = {-3.34406784, 4.23886395, -2.40934286, 0.5174782};
float b[] = {0.00018322, 0.00073286, 0.0010993, 0.00073286, 0.00018322};


void setup() {

  frequency = 0;

  current_time = 0;
  past_time_pressure = 0;
  past_time_flow = 0;

  volumeTotal = 0;

  uint32_t baudrate = 115200;
  Serial.begin( baudrate, SERIAL_8N1 );

  attachInterrupt( digitalPinToInterrupt( PIN_SENSOR_FLOW ), 
                  getFrequency, 
                  FALLING );

  initialize();
  calibrateSensor();
}

void loop() {

  /*while(1){
    u[ SIZE_B - 1 ] = getVolume() - calibrate_pressure;
    y[ SIZE_A ] = sum_zeros() - sum_polos();
    shifty();
    //Serial.println( getVolume() - calibrate_pressure );
    Serial.print( getVoltage() );
    Serial.print( "\t" );
    Serial.print( getVolume() );
    Serial.print( "\t" );
    Serial.println( calibrate_pressure );
    
    delay( 200 );  
  }*/

  current_time = millis();
  uint64_t var_time_pressure  = current_time - past_time_pressure;
  uint64_t var_time_flow      = current_time - past_time_flow;

  if( var_time_pressure > TIME_COLLECT_PRESSURE ){

    u[ SIZE_B - 1 ] = getVolume() - calibrate_pressure;
    y[ SIZE_A ] = sum_zeros() - sum_polos();
    shifty();    
    
    String data = ";p " + String(current_time / 1000.0) + "," + String( y[ SIZE_A ] );
    //String data = ";p " + String(current_time / 1000.0) + "," + String( getVolume() - calibrate_pressure );
    
    past_time_pressure = current_time;
    Serial.println( data );
  }
  
  if( var_time_flow > TIME_COLLECT_FLOW ){
    cli();
    float flow_L4min = frequency * 4 / float(CALIBRATION_FLOW);    
    float flow_ml4sec = flow_L4min * 1000.0 / 60.0;

    volumeTotal += flow_ml4sec * 0.25;
    frequency = 0;

    String data = ";f " + String( current_time / 1000.0 ) + "," + String( volumeTotal );
    Serial.println( data );


    past_time_flow = current_time;
    sei();
  }
}

static float getVoltage(){
  uint16_t sample = analogRead( PIN_SENSOR_PRESSURE );
  uint16_t voltage_mV = map( sample, 0,1024,0,5000 );

  float voltage_V = voltage_mV / 1000.0;

  return voltage_V;
}

static void calibrateSensor(){
  calibrate_pressure = 0;
  for( int i = 0; i < SAMPLE_CALIBRATION; i++ ){
    calibrate_pressure += getVolume();   
  }

  calibrate_pressure /= float(SAMPLE_CALIBRATION);
}

static float getVolume(){

    float x = getVoltage();
    float a = 246.65;
    float b = -387.69;
    
    float volume = x * a + b;

    if( volume <= 0 )
      volume = 0;

    return volume;  
}

static void getFrequency(){ frequency++; }

void initialize(){
    for( int i = 0; i < SIZE_B; i++ )
       u[i] = 0; 

    for( int i = 0; i < SIZE_A; i++ )
       y[i] = 0; 
}

float sum_zeros(){
    float uv = 0;
    for( int i = 0; i < SIZE_B; i++ )
        uv += b[i]*u[SIZE_B - i - 1];
    shiftu();
    return uv;
}

float sum_polos(){
    float yv = 0;
    for( int i = 0; i < SIZE_A; i++ )
        yv += a[i]*y[SIZE_A - i - 1];
    return yv;
}


void shiftu(){
    for( int i = 0; i < SIZE_B-1; i++ )
        u[i] = u[i+1];
}

void shifty(){
    for( int i = 0; i < SIZE_A; i++ )
        y[i] = y[i+1];
}
