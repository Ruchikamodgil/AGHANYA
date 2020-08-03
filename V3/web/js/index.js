var firebaseConfig = {
    apiKey: "AIzaSyDienGaKvTKGuSgKIFsU1pupYC1DABpeYk",
    authDomain: "aghanya-test-py.firebaseapp.com",
    databaseURL: "https://aghanya-test-py.firebaseio.com",
    projectId: "aghanya-test-py",
    storageBucket: "aghanya-test-py.appspot.com",
    messagingSenderId: "356482709357",
    appId: "1:356482709357:web:ba6a50f651806c23660c64",
    measurementId: "G-688BED1Y8M"
  };
  // Initialize Firebase
  firebase.initializeApp(firebaseConfig);
  firebase.analytics();

  firebase.auth.Auth.Persistence.LOCAL;

  $("#btn-login").click(function(){
      var email = $("#email").val();
      var password = $("#password").val();

      if(email != "" && password != ""){
        var result = firebase.auth().signInWithEmailAndPassword(email,password);

        result.catch(function(error){
          var errorCode = error.code;
          var errorMsg = error.message;
          window.alert("Message : " + errorMsg);
        })
      }else{
        window.alert("Please fill out all the fields.");
      }
  });

  $("#btn-signup").click(function(){
      var email = $("#email").val();
      var password = $("#password").val();
      var cPassword = $("#confirmPassword").val();
      if(email != "" && password != "" && cPassword != ""){
        if(password == cPassword){
            var result = firebase.auth().createUserWithEmailAndPassword(email,password);

            result.catch(function(error){
              var errorCode = error.code;
              var errorMsg = error.message;
              window.alert("Message : " + errorMsg);
            })
          }else{
            window.alert("Password not match with Confirm Password.");
          }
        }else{
          window.alert("Please fill out all the fields.");
        }
  });

  $("#btn-resetPassword").click(function(){
    var auth = firebase.auth();
    var email =  $("#email").val();
    if(email != ""){
        auth.sendPasswordResetEmail(email).then(function(){
          window.alert("Email has been send to you, Please check and verify");
        })
        .catch(function(error){
          var errorCode = error.code;
          var errorMsg = error.message;
          window.alert("Message : " + errorMsg);
        });
    }else{
      window.alert("Please fill out the email");
    }
  });

  $("#btn-logout").click(function(){
    firebase.auth().signOut();    
  });

  $("#btn-update").click(function(){
      var fName = $("#firstName").val();
      var sName = $("#secondName").val();
      var phone = $("#phone").val();
      var country = $("#country").val(); 
      var gender = $("#gender").val();   
      var address = $("#address").val();

      var rootRef = firebase.database().ref().child("Users");
      var userID = firebase.auth().currentUser.uid;
      var userRef = rootRef.child(userID);

      if(fName != "" && sName != "" && phone != "" && country != "" && gender != "" && address != ""){
          var userData = {
              "phone" : phone,
              "fName" : fName,
              "sName" : sName,
              "country" : country,
              "gender" : gender,
              "address" : address
          };

          userRef.set(userData, function(error){
            if(error){
              var errorCode = error.code;
              var errorMsg = error.message;
              window.alert("Message : " + errorMsg);             
            }else{
              window.location.href = "MainPage.html";
            }
          });
      }else{
        window.alert("Please fill out all the fields");
      }
  });