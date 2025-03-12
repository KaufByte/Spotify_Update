import React, { useEffect, useState } from 'react';
import './Layout.css';
import { FaHome, FaSearch, FaBell } from 'react-icons/fa';
import AvatarMenu from './AvatarMenu';

interface LayoutProps {
  setSearchTerm: (term: string) => void; 
}

const Layout: React.FC<LayoutProps> = ({ setSearchTerm }) => {
  const [userEmail, setUserEmail] = useState<string | null>(null); 

  useEffect(() => {
    const email = localStorage.getItem("userEmail");
    setUserEmail(email);
  }, []);

  const handleHomeClick = () => {
    window.location.reload(); // 🔥 Обновление страницы при нажатии
  };

  return (
    <div className="spotify-header">
      <div className="header-left">
        <img
          src="https://storage.googleapis.com/pr-newsroom-wp/1/2023/05/Spotify_Primary_Logo_RGB_White.png"
          alt="Spotify Logo"
          className="spotify-logo"
        />
      </div>

      <div className="header-center">
        <div className="home-button" onClick={handleHomeClick}>
          <FaHome className="icon home-icon" />
        </div>
        
        <div className="search-wrapper">
          <input
            type="text"
            placeholder="Что вы хотите послушать?"
            className="search-input"
            onChange={(e) => setSearchTerm(e.target.value)} 
          />
          <FaSearch className="search-icon" />
        </div>
      </div>

      <div className="header-right">
        <div className='Bell'>
          <FaBell className="icon-bell" />
        </div>
        <div className='avatar'>
          <AvatarMenu/>
        </div>
      </div>
    </div>
  );
};

export default Layout;
