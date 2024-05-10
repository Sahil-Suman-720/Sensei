import express from 'express';
import bodyParser from 'body-parser';
import axios from 'axios';
const app = express();
const port = 4000;


//     name : "Shashi Tharoor",
//     experience: "26",
//     img:"shashi_tharoor.png",
//     subjects: "English"
//    },{
//     name : "Alakh Pandey",
//     experience: "10",
//     img:"alakh_pandey.png",
//     subjects: "Physics"
//    },   
const teaches = [ 
    {
        "name": "Amit Sharma",
        "experience": 3,
        "subjects": "maths biology",
        "education_level": "student",
        "img": "Amit_Sharma.png"
      },
      {
        "name": "Priya Patel",
        "experience": 6,
        "subjects": "music",
        "education_level": "undergraduate",
        "img": "Priya_Patel.png"
      },
      {
        "name": "Rahul Kumar",
        "experience": 10,
        "subjects": "physics",
        "education_level": "post graduate",
        "img": "Rahul_Kumar.png"
      },
      {
        "name": "Sneha Singh",
        "experience": 15,
        "subjects": "maths biology physics",
        "education_level": "phd",
        "img": "Sneha_Singh.png"
      },
      {
        "name": "Rohit Gupta",
        "experience": 2,
        "subjects": "biology english",
        "education_level": "student",
        "img": "Rohit_Gupta.png"
      },
      {
        "name": "Neha Reddy",
        "experience": 5,
        "subjects": "maths physics",
        "education_level": "undergraduate",
        "img": "Neha_Reddy.png"
      },
      {
        "name": "Sachin Verma",
        "experience": 12,
        "subjects": "biology music",
        "education_level": "post graduate",
        "img": "Sachin_Verma.png"
      },
      {
        "name": "Anjali Kapoor",
        "experience": 18,
        "subjects": "music physics",
        "education_level": "phd",
        "img": "Anjali_Kapoor.png"
      },
      {
        "name": "Vivek Mishra",
        "experience": 4,
        "subjects": "maths biology english",
        "education_level": "student",
        "img": "Vivek_Mishra.png"
      },
      {
        "name": "Pooja Singh",
        "experience": 8,
        "subjects": "music maths",
        "education_level": "undergraduate",
        "img": "Pooja_Singh.png"
      },
      {
        "name": "Rajesh Khanna",
        "experience": 14,
        "subjects": "physics english",
        "education_level": "post graduate",
        "img": "Rajesh_Khanna.png"
      },
      {
        "name": "Swati Joshi",
        "experience": 17,
        "subjects": "maths biology music",
        "education_level": "phd",
        "img": "Swati_Joshi.png"
      },
      {
        "name": "Aryan Sharma",
        "experience": 2,
        "subjects": "music physics",
        "education_level": "student",
        "img": "Aryan_Sharma.png"
      },
      {
        "name": "Shreya Gupta",
        "experience": 7,
        "subjects": "biology english",
        "education_level": "undergraduate",
        "img": "Shreya_Gupta.png"
      },
      {
        "name": "Kunal Patel",
        "experience": 11,
        "subjects": "maths physics",
        "education_level": "post graduate",
        "img": "Kunal_Patel.png"
      }
    ];


app.use(express.static("public"));
app.use(bodyParser.urlencoded({extended:true}));

app.get("/",(req,res) =>
res.render("index.ejs"));

// app.get("/home",(req,res)=>
//     {
//         res.render("home.ejs",{posts:teaches});
//     });

app.get("/register",(req,res)=>
{
    res.render("register.ejs");
});

app.get("/register_t",(req,res)=>
{
    res.render("register_t.ejs");
});

app.get("/login",(req,res)=>
{
    res.render("login.ejs");
});

app.post("/login_submit",async (req,res) =>
{
    let data = req.body;
   console.log(data)
   try{
    const go = await axios.post("http://localhost:5000/chkpwd",data);
    if (go.data[1] === false)
        res.render("login.ejs",{message:"Invalid credentials"});
    else
        res.render("home.ejs",{user:go.data[0],posts:teaches});
    }
    catch(err){console.log("went wrong");}
});

app.post("/submit",async (req,res) =>{
const data = req.body;
var header = 0;
const send = {};
var intr = "";
for(const key in data)
{   
    header += 1;
    if(header > 5){
        intr += key+" ";
    console.log(key)}
    else{
        send[key] = data[key];
    }
}
send['interests'] = intr.slice(0,intr.length-1);
const go = await axios.post("http://localhost:5000/signup",send);
if(go.data === "ok")
res.render("index.ejs",{alert:"Student Registration Successful"})
});


app.post("/submit_t",async (req,res) =>{
    const data = req.body;
    var header = 0;
    const send = {};
    var intr = "";
    for(const key in data)
    {   
        header += 1;
        if(header > 6){
            intr += key+" ";
        console.log(key)}
        else{
            send[key] = data[key];
        }
    }
    send['subjects'] = intr.slice(0,intr.length-1);
    const go = await axios.post("http://localhost:5000/signup_t",send);
    res.sendStatus(200);});

app.listen(port,()=>
{
    console.log(`Server listening at http://localhost:${port}`);
});