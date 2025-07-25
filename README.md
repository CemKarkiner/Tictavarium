# An application for guitarist to practice

## To Do List
- Metronome (DONE)
- Database (SQL or NoSQL)(DONE)
- Interface Design (Done)
- Good interface (continues)
- Tab-metronome integration
- Reading tabs via Audiveris to read and convert the data from musicxml to JSON data (Audiveris-gradle) (Audiveris converts PDF to note wrong! We need to read from tabs not notes)
- Deployment (Docker, Kubernet, Prometeus etc.)
- Note correction while playing (Optional)
## Music Side
- Primary focus is guitar
- User can set the metronome settings (Done)
- Music measure needs to be change automaticly (3/4, 4/4 etc.)
- Default metronome should be the original metronome of S&P  
- User can slow down the music metronome (Done)
- Guitar sound frequences should be implemented (24 frets) (Done)
- 1/2 notes, 1/4 notes etc. (mandatory)
## Application side
### Backend
- All project will be develop in python (subproceses can change)
- Application needs to contain S&Ps (songs and practices)
- Database will hold the data of the S&Ps (will improve)
- The song needs to start from its original BPM as a default but user should be able to change
- The software needs to identify the new tabs using audiveris subprocess 
- Offline and online mods should be provided 
- The S&Ps should have backtrackings that stored in S3 
### Frontend
- Application needs to have a administor interface that uploads new S&Ps via PDF
- Music tabs and notes should be shown
- There needs to be a bar to show user where they are (Done but need to be better)
- Tabs, notes and bar should work in synchronized
- User can search the songs from an upper search bar (DONE)
- User can set the metronome from upper left corner (DONE)
### Tech Stack
| Component  | Choice |
| ------------- | ------------- |
| Database   | MongoDB |
| Backend  | FastAPI |
| Frontend  | TypeScript |
| File Storage  | S3 |
| Monitoring  | Prometheus + Grafana |
| Deployment  | Docker + Docker Compose / Kubernetes |
| Hosting  | EC2 |

