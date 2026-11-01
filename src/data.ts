export type InningsScore={team:string,runs:number,wickets:number,overs:string,legalBalls:number};
export type LiveMatch={id:string,name:string,home:string,away:string,homeCode:string,awayCode:string,format:string,competition:string,venue:string,status:string,dateTimeGMT:string,battingTeam:string,bowlingTeam:string,innings:InningsScore[],runs:number,wickets:number,overs:string,legalBalls:number,target:number|null,runsRequired:number|null,ballsRemaining:number|null,currentRunRate:number|null,requiredRunRate:number|null,summary:string,live:true};
export type Experience='Beginner'|'Casual'|'Regular'|'Expert';
export type ChatTurn={role:'user'|'buddy',text:string};
export const abbreviate=(team:string)=>team.split(/\s+/).map(part=>part[0]||'').join('').slice(0,3).toUpperCase();
export const formatRate=(runs:number,balls:number)=>balls>0?(runs*6/balls).toFixed(2):null;
export const legalBallsFromOvers=(overs:string|number)=>{const [whole,part='0']=String(overs).split('.');const completed=Number.parseInt(whole,10);const balls=Number.parseInt(part,10);if(!Number.isFinite(completed)||!Number.isFinite(balls)||balls<0||balls>5)return 0;return completed*6+balls};
