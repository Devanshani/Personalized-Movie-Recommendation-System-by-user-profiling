using FrontEnd_Version1.Models;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.Mvc;

namespace FrontEnd_Version1.Controllers
{
    public class AccountController : Controller
    {
        // GET: Account
        public ActionResult Index()
        {
            using (FrontEndDB db = new FrontEndDB())
            {

                var userId = Convert.ToDecimal(Session["UserId"]);
                return View(db.UserInfoes.Where(t => t.Id == userId).ToList());
            }
        }

        public new ActionResult Profile()
        {
            using (FrontEndDB db = new FrontEndDB())
            {

                var userId = Convert.ToDecimal(Session["UserId"]);
                return View(db.UserInfoes.Where(t => t.Id == userId).ToList());

            }
        }
      
        public ActionResult Register()
        {

            return View();
        }
        [HttpPost]
        public ActionResult Register(UserInfo account)
        {
            if (ModelState.IsValid)
            {
                using (FrontEndDB db = new FrontEndDB())
                {
                    db.UserInfoes.Add(account);
                    db.SaveChanges();
                }
                ModelState.Clear();
                ViewBag.Message = account.UserName + "successfully registred";
                return RedirectToAction("Login");
            }
            return View();

        }


        public ActionResult Login()
        {
            return View();
        }
        [HttpPost]
        public ActionResult Login(UserInfo user)
        {
            using (FrontEndDB db = new FrontEndDB())
            {
                var usr = db.UserInfoes.Single(u => u.UserName == user.UserName && u.Password == user.Password);
                if (usr != null)
                {
                    Session["UserId"] = usr.Id.ToString();
                    Session["Username"] = usr.UserName.ToString();
                    return RedirectToAction("Profile");

                }
                else
                {
                    ModelState.AddModelError("", "Email or password is wrong");
                }
            }
            return View();
        }
        public ActionResult LoggedIn()
        {
            if (Session["UserId"] != null)
            {
                return View();
            }
            else
            {
                return RedirectToAction("Profile");
            }
        }
        public ActionResult Reccomend()
        {
            
            
                return RedirectToAction("Index");
            
        }

        public ActionResult NewRegister()
        {

            return View();
        }







        [HttpPost]
        public ActionResult NewRegister(UserInfo account)
        {
            if (ModelState.IsValid)
            {
                using (FrontEndDB db = new FrontEndDB())
                {
                    db.UserInfoes.Add(account);
                    db.SaveChanges();
                }
                ModelState.Clear();
                ViewBag.Message = account.UserName + "successfully registred";
                return RedirectToAction("NewLogin");
            }
            return View();

        }

        public ActionResult NewLogin()
        {
            return View();
        }
        [HttpPost]
        public ActionResult NewLogin(UserInfo user)
        {
            using (FrontEndDB db = new FrontEndDB())
            {
                var usr = db.UserInfoes.Single(u => u.UserName == user.UserName && u.Password == user.Password);
                if (usr != null)
                {
                    Session["UserId"] = usr.Id.ToString();
                    Session["Username"] = usr.UserName.ToString();
                    return RedirectToAction("NewRecomend");

                }
                else
                {
                    ModelState.AddModelError("", "Email or password is wrong");
                }
            }
            return View();
        }
        public ActionResult NewLoggedIn()
        {
            if (Session["UserId"] != null)
            {
                return View();
            }
            else
            {
                return RedirectToAction("NewRecomend");
            }
        }
        public ActionResult NewRecomend()
        {
            using (FrontEndDB db = new FrontEndDB())
            {

                var userId = Convert.ToDecimal(Session["UserId"]);
                return View(db.UserInfoes.Where(t => t.Id == userId).ToList());
            }
        }

    }
}