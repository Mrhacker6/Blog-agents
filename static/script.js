const g=id=>document.getElementById(id);
let md="",download="";
const fill=g("fill");
const steps=["Researching videos...","Analyzing transcripts...","Writing blog...","Formatting output..."];
g("generate").onclick=async()=>{
g("error").textContent="";
g("status").classList.remove("hidden");
fill.style.width="5%";
let i=0;
const t=setInterval(()=>{
fill.style.width=((i+1)*25)+"%";
g("statusText").textContent=steps[Math.min(i,steps.length-1)];
i++;
},1200);
try{
const res=await fetch("/generate",{
method:"POST",
headers:{"Content-Type":"application/json"},
body:JSON.stringify({channel:g("channel").value,topic:g("topic").value})
});
const data=await res.json();
clearInterval(t);
fill.style.width="100%";
if(!res.ok) throw new Error(data.detail||"Generation failed");
md=data.blog;
download=data.download_url;
g("blog").innerHTML=marked.parse(md);
}catch(e){
clearInterval(t);
g("error").textContent=e.message;
}
};
g("copy").onclick=()=>navigator.clipboard.writeText(md);
g("download").onclick=e=>{
e.preventDefault();
if(download) window.location=download;
};