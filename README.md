# Conad Simulator

## A discrete-event simulator of a CONAD supermarket

### Overview
This is made for a university project. Our aim is to create a discrete-event simulator to model a CONAD supermarket and analyse some variables of interest (like the mean waiting time). Below there is the full text of the assigment (in italian).

Il gestore del vostro supermercato (CONAD) ha problemi per determinare il numero di cassiere da avere in uno dei periodi di maggiore affluenza.
Poiché tua madre si lagna spesso delle attese alla cassa e ti ha sfidato a mettere in pratica la tua preparazione sulla teoria delle code, tu ti incarichi del compito di aiutare il gestore.
Decidi quindi – a causa della complessità di decisione e di diniego, dell’abilità di aggiungere o togliere cassiere  (che incrementano o decrementano il μ di canale) e altre complessità – di simulare il modello di sistema.
Sviluppa il modello di simulazione e implementalo nel linguaggio che tu desideri.
Tenta di stimare, a partire da tue reali osservazioni su alcuni sabati mattina, i modelli di arrivo e di servizio, così come la disciplina delle code.
Usa parte delle osservazioni per sviluppare le distribuzioni empiriche e convalida poi il simulatore usando le rimanenti osservazioni (al 90% del livello di confidenza). 
Quindi cerca di determinare le soluzioni per i problemi del gestore.

We used Python 2.7.10 and the SimPy library. Methods to find a steady-state and to statistically validate the simulator are provided. All statistical data had been taken from the real environment and validated using the Goodness of Fit method. NumPy and MatPlotLib libraries for Python are also required.

### How it works
The simulator is represented by the **ConadSimulator** class. The SimPy library provides a simulation environment usable via the **simpy.Environment()** method, that can handle events and their enqueuing or limited resources contended by the users of the system. We represented every single cash register as a limited resource of capacity 1 (calling **simpy.Resource()**). There is an istance of the method **entrance()** (run over the Environment using the **Environment.process()** method) that randomly generates new customers enqueuing the cash registers according to the negative exponential distribution observed and validated during the data acquisition phase and runs them over the Environment (again with the **Environment.process()** method). Every customer is represented as an istance of the **customer()** method, that simply chooses one of the cash registers and waits to use it (a process can be scheduled for a posterior time using the **yield** Python keyword). When it comes to the chosen cash register, it uses it for a time generated from a gaussian distribution (again observed and validated from the real data before), then it leaves the system. At the end of the simulation time (**Environment.run(until=duration)** lets you decide for how many time units the simulation had to go on) various statistical variables of interest are computed and printed. The **stabilize()** method compute a minimum duration time from which on the influence of the initial arbitrary state on the analysis of the simulation results becomes small, while the **repeated_measures()** one checks if the simulator is validable.

### Author
*Castellini Jacopo*
