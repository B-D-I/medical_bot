# medical_bot
v2 - includes camera


IGNORE ALL SCRATCH FILES, THESE INCLUDED FUNCTIONS UNECCESSARY OR BEYOND THE SCOPE OF THE DISSERTATION RESEARCH:
- heart rate sensor
- SQLite database
- web scraping
- user CRUD functions
- time / date / chatbot functions etc.

Code is reduced and only allows for patient data to be kept in volatile memory for security

\begin{table}[H]
\caption{Hardware}\label{tbl:hardware}
\centering
\begin{tabular}{|l|l|l|}
\hline
\textbf{} & \textbf{Component} & \textbf{Requirement} \\ \hline
1 & Raspberry Pi 4 model B (8gb) & \begin{tabular}[c]{@{}l@{}}Single-board computer for running\\ DL model and software\end{tabular} \\ \hline
2 & Raspberry Pi high-quality camera module & \begin{tabular}[c]{@{}l@{}}Enable high-quality camera images\\ for classification\end{tabular} \\ \hline
3 & 8-50mm zoom lens HQ & \begin{tabular}[c]{@{}l@{}}Enable capturing of high-quality\\ macroscopic images\end{tabular} \\ \hline
4 & Mini tripod & Provide stability for the camera \\ \hline
5 & ReSpeaker 4 mic array & Microphone to enable voice contol \\ \hline
6 & Mini external USB speaker & Provide audio for voice control \\ \hline
7 & XL Raspberry Pi heatsink & Reduce CPU heat \\ \hline
8 & \begin{tabular}[c]{@{}l@{}}Elegoo Uno + mini breadboard, buzzer\\ and LEDs\end{tabular} & \begin{tabular}[c]{@{}l@{}}Enable additional functionality\\ such as an alarm and LED \\ user-indications\end{tabular} \\ \hline
9 & Elecrow 7-inch touchscreen & \begin{tabular}[c]{@{}l@{}}Enable user image to be viewed\\ before capture\end{tabular} \\ \hline
\end{tabular}
\end{table}

![schema](https://user-images.githubusercontent.com/85758021/211778780-f83d727b-d685-4f49-926f-8d3c187e60dd.png)
