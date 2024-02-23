# medical_bot

<br/>
<b>Enables patient medical image to be captured, then classified for MPXV, normal, or other skin condition. Then the diagnosis and accompanying data is sent via email to specified address.</b> 
<br/>
<br/>
IGNORE ALL SCRATCH FILES, THESE INCLUDED FUNCTIONS ARE BEYOND THE SCOPE OF THE DISSERTATION RESEARCH<br/><br/>
SUCH AS:<br/>
- heart rate sensor<br/>
- Infermedica API diagnosis<br/>
- SQLite database<br/>
- web scraping<br/>
- user CRUD functions<br/>
- time / date / chatbot functions etc.<br/>
<br/>
Code is reduced and only allows for patient data to be kept in volatile memory for security <br/>
<br/>
SCHEMATIC
<br/>
1: Raspberry Pi 4 model B (8gb) - Single-board computer for running DL model and software<br/>
2: Raspberry Pi high-quality camera module - Enable high-quality camera images for classification<br/>
3: 8-50mm zoom lens HQ - Enable capturing of high-quality macroscopic images<br/>
4: Mini tripod - Provide stability for the camera <br/>
5: ReSpeaker 4 mic array - Microphone to enable voice contol <br/>
6: Mini external USB speaker - Provide audio for voice control<br/>
7: XL Raspberry Pi heatsink - Reduce CPU heat <br/>
8: Elegoo Uno + mini breadboard, buzzer and LEDs - Enable additional functionality, such as an alarm and LED, user-indications <br/>
9: Elecrow 7-inch touchscreen - Enable user image to be viewed before capture<br/>
<br/>

![schema](https://user-images.githubusercontent.com/85758021/211778780-f83d727b-d685-4f49-926f-8d3c187e60dd.png)
