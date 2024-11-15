import { createRoot } from 'react-dom/client'
import 'react-toastify/dist/ReactToastify.css';
import App from './App.jsx'
import './index.css'
import LogoutPage from "./pages/LogoutPage/LogoutPage.jsx";
import RegisterPage from "./pages/RegisterPage/RegisterPage.jsx";
import LoginPage from "./pages/LoginPage/LoginPage.jsx";
import {createBrowserRouter, RouterProvider} from "react-router-dom";
import {ToastContainer} from "react-toastify";
import ProfilePage from "./pages/ProfilePage/ProfilePage.jsx";
import LoginRequiredRoute from "./utils/LoginRequiredRoute.jsx";
import ContestListPage from "./pages/ContestListPage/ContestListPage.jsx";
import ContestDetailPage from "./pages/ContestDetailPage/ContestDetailPage.jsx";
import {MuiThemeProvider} from "@material-ui/core";
import theme from "./theme.jsx";
import QuizSolutionDetailPage from "./pages/SolutionDetailPage/QuizSolutionDetailPage.jsx";
import CodeSolutionDetailPage from "./pages/SolutionDetailPage/CodeSolutionDetailPage.jsx";
import HelpPage from "./pages/HelpPage/HelpPage.jsx";
import LocalSettingsPage from "./pages/LocalSettingsPage/LocalSettingsPage.jsx";
import EditQuizTaskPage from "./pages/EditTaskPage/EditQuizTaskPage.jsx";
import EditCodeTaskPage from "./pages/EditTaskPage/EditCodeTaskPage.jsx";
import EditTextPage from "./pages/EditTaskPage/EditTextPage.jsx";
import EditContestPage from "./pages/EditContestPage/EditContestPage.jsx";
import ContestStandingsPage from "./pages/ContestStandingsPage/ContestStandingsPage.jsx";

const router = createBrowserRouter([
    {
        path: '/',
        element: <App/>,
        children: [
            {
                path: "/profile",
                element: <LoginRequiredRoute><ProfilePage/></LoginRequiredRoute>
            },
            {
                path: "/profile/:page",
                element: <LoginRequiredRoute><ProfilePage/></LoginRequiredRoute>
            },
            {
                path: "/contests",
                element: <LoginRequiredRoute><ContestListPage/></LoginRequiredRoute>
            },
            {
                path: "/contests/:contestId",
                element: <LoginRequiredRoute><ContestDetailPage/></LoginRequiredRoute>
            },
            {
                path: "/contests/:contestId/standings",
                element: <LoginRequiredRoute><ContestStandingsPage/></LoginRequiredRoute>
            },
            {
                path: "/contests/:contestId/edit",
                element: <LoginRequiredRoute><EditContestPage/></LoginRequiredRoute>
            },
            {
                path: "/contests/:contestId/:pageType/:pageId",
                element: <LoginRequiredRoute><ContestDetailPage/></LoginRequiredRoute>
            },
            {
                path: "/contests/:contestId/quiz/:pageId/edit",
                element: <LoginRequiredRoute><EditQuizTaskPage/></LoginRequiredRoute>
            },
            {
                path: "/contests/:contestId/code/:pageId/edit",
                element: <LoginRequiredRoute><EditCodeTaskPage/></LoginRequiredRoute>
            },
            {
                path: "/contests/:contestId/text/:pageId/edit",
                element: <LoginRequiredRoute><EditTextPage/></LoginRequiredRoute>
            },
            {
                path: "/solutions/quiz/:solutionId",
                element: <LoginRequiredRoute><QuizSolutionDetailPage/></LoginRequiredRoute>
            },
            {
                path: "/solutions/code/:solutionId",
                element: <LoginRequiredRoute><CodeSolutionDetailPage/></LoginRequiredRoute>
            },
            {
                path: "/help",
                element: <LoginRequiredRoute><HelpPage/></LoginRequiredRoute>
            },
            {
                path: "/local-settings",
                element: <LoginRequiredRoute><LocalSettingsPage/></LoginRequiredRoute>
            }
        ]
    },
    {
        path: "/login",
        element: <LoginPage/>
    },
    {
        path: "/register",
        element: <RegisterPage/>
    },
    {
        path: "/logout",
        element: <LogoutPage/>
    }
]);

createRoot(document.getElementById('root')).render(
  //<StrictMode>
      <>
          <MuiThemeProvider theme={theme}>
              <RouterProvider router={router}></RouterProvider>

              <ToastContainer
                  position="bottom-right"
                  hideProgressBar={false}
                  newestOnTop={false}
                  closeOnClick={true}
                  rtl={false}
                  pauseOnHover={true}
                  draggable={false}
                  theme="colored"
              />
          </MuiThemeProvider>
      </>
  //</StrictMode>,
)
