# An application for musicians to practice
## Do List (In order)
- Metronome (Done)
- Reading tabs and converting into data
- Tab-metronome integration
- Good interface
- Database (SQL or NoSQL)
- Possible Cloud Technologies (AWS)
- Deployment (Docker, Kubernet, Prometeus etc.)
- Note correction while playing (Optional)
- ER diagram and flow chart needs to be drawn

## Music Side
- Primary focus is guitar
- User can set the metronome settings
- User can slow down the music metronome
- Guitar sound frequences should be implemented (24 frets)
- 1/2 notes, 1/4 notes etc. (mandatory)

## Application side
### Backend
- All project will be develop in python (subprocess can change)
- Application needs to contain S&Ps (songs and practices)
- Database will hold the data of the S&Ps
- The song needs to start from its original BPM as a default but user should be able to change
- The software needs to identify the new tabs using audiveris subprocess
- Offline and online mods should be provided (optional)
- The S&Ps should have backtrackings (optional)

### Frontend
- Application needs to have a administor interface that uploads new S&Ps via PDF
- Music tabs and notes should be shown
- There needs to be a bar to show user where they are
- Tabs, notes and bar should work in synchronized
- User can search the songs from an upper search bar
- User can set the metronome from upper left corner 

## Tech Stack
| Component  | Choice |
| ------------- | ------------- |
| Database  | MongoDB  |
| Backend  | FastAPI  |
| Frontend  | Vue  |
| File Storage  | S3 |
| Monitoring  | Prometheus + Grafana  |
| Deployment  | Docker + Docker Compose / Kubernetes |
| Hosting  | EC2  |
