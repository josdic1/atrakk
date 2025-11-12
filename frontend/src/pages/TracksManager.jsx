import { useState, useEffect } from 'react';
import { Music, Plus, Tag, Link as LinkIcon, Trash2, ExternalLink, Music2, Video, Image, FileText, Globe, Search, Edit, Eye, Filter } from 'lucide-react';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5555';

function TracksManager() {
  const [tracks, setTracks] = useState([]);
  const [artists, setArtists] = useState([]);
  const [statuses, setStatuses] = useState([]);
  const [tags, setTags] = useState([]);

  const [viewMode, setViewMode] = useState(null); // 'view', 'edit', or 'filter'
  const [selectedTrack, setSelectedTrack] = useState(null);
  const [filteredTracks, setFilteredTracks] = useState([]);
  
  const [newTrack, setNewTrack] = useState({ title: '', artist_id: '', status_id: '' });
  const [showLinkForm, setShowLinkForm] = useState(null);
  const [newLink, setNewLink] = useState({ link_type: '', link_url: '' });
  
  const [newArtist, setNewArtist] = useState('');
  const [showArtistForm, setShowArtistForm] = useState(false);

  const [editForm, setEditForm] = useState({ title: '', artist_id: '', status_id: '' });

  const [newTag, setNewTag] = useState('');
  const [showTagForm, setShowTagForm] = useState(false);

  const [searchQuery, setSearchQuery] = useState('');
  const [activeFilter, setActiveFilter] = useState(null);

  useEffect(() => {
    fetchTracks();
    fetchArtists();
    fetchStatuses();
    fetchTags();
  }, []);

  const getLinkIcon = (linkType) => {
    const type = linkType.toLowerCase();
    if (type.includes('spotify') || type.includes('music') || type.includes('soundcloud')) {
      return <Music2 size={14} />;
    }
    if (type.includes('youtube') || type.includes('video')) {
      return <Video size={14} />;
    }
    if (type.includes('artwork') || type.includes('cover') || type.includes('image')) {
      return <Image size={14} />;
    }
    if (type.includes('lyrics') || type.includes('doc')) {
      return <FileText size={14} />;
    }
    return <Globe size={14} />;
  };

  const getStatusColor = (statusName) => {
    const colors = {
      'Idea': '#666',
      'Demo': '#3b82f6',
      'In Progress': '#eab308',
      'Completed': '#22c55e',
      'Released': '#a855f7'
    };
    return colors[statusName] || '#666';
  };

  const fetchTracks = async () => {
    const res = await fetch(`${API_BASE_URL}/tracks`);
    const data = await res.json();
    setTracks(data);
  };

  const fetchArtists = async () => {
    const res = await fetch(`${API_BASE_URL}/artists`);
    const data = await res.json();
    setArtists(data);
  };

  const fetchStatuses = async () => {
    const res = await fetch(`${API_BASE_URL}/command/data`);
    const data = await res.json();
    setStatuses(data.statuses);
  };

  const fetchTags = async () => {
    const res = await fetch(`${API_BASE_URL}/tags`);
    const data = await res.json();
    setTags(data);
  };

  const createTrack = async (e) => {
    e.preventDefault();
    const res = await fetch(`${API_BASE_URL}/tracks`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(newTrack)
    });
    
    if (res.ok) {
      setNewTrack({ title: '', artist_id: '', status_id: '' });
      fetchTracks();
    }
  };

  const addTagToTrack = async (trackId, tagId) => {
    const res = await fetch(`${API_BASE_URL}/tracks/${trackId}/tags/${tagId}`, {
      method: 'POST'
    });
    
    if (res.ok) {
      fetchTracks();
      if (selectedTrack?.id === trackId) {
        const updated = await fetch(`${API_BASE_URL}/tracks/${trackId}`);
        const data = await updated.json();
        setSelectedTrack(data);
      }
    }
  };

  const removeTagFromTrack = async (trackId, tagId) => {
    if (confirm('Are you sure you want to remove this tag?')) {
      const res = await fetch(`${API_BASE_URL}/tracks/${trackId}/tags/${tagId}`, {
        method: 'DELETE'
      });
      
      if (res.ok) {
        fetchTracks();
        if (selectedTrack?.id === trackId) {
          const updated = await fetch(`${API_BASE_URL}/tracks/${trackId}`);
          const data = await updated.json();
          setSelectedTrack(data);
        }
      }
    }
  };

  const addLinkToTrack = async (trackId) => {
    const res = await fetch(`${API_BASE_URL}/tracks/${trackId}/links`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(newLink)
    });
    
    if (res.ok) {
      setNewLink({ link_type: '', link_url: '' });
      setShowLinkForm(null);
      fetchTracks();
      if (selectedTrack?.id === trackId) {
        const updated = await fetch(`${API_BASE_URL}/tracks/${trackId}`);
        const data = await updated.json();
        setSelectedTrack(data);
      }
    }
  };

  const removeLink = async (linkId) => {
    if (confirm('Are you sure you want to delete this link?')) {
      const res = await fetch(`${API_BASE_URL}/links/${linkId}`, {
        method: 'DELETE'
      });
      
      if (res.ok) {
        fetchTracks();
        if (selectedTrack) {
          const updated = await fetch(`${API_BASE_URL}/tracks/${selectedTrack.id}`);
          const data = await updated.json();
          setSelectedTrack(data);
        }
      }
    }
  };

  const createArtist = async (e) => {
    e.preventDefault();
    const res = await fetch(`${API_BASE_URL}/artists`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name: newArtist })
    });
    
    if (res.ok) {
      setNewArtist('');
      setShowArtistForm(false);
      fetchArtists();
    }
  };

  const updateTrackStatus = async (trackId, statusId) => {
    const res = await fetch(`${API_BASE_URL}/tracks/${trackId}`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ status_id: statusId })
    });
    
    if (res.ok) {
      fetchTracks();
      if (selectedTrack?.id === trackId) {
        const updated = await fetch(`${API_BASE_URL}/tracks/${trackId}`);
        const data = await updated.json();
        setSelectedTrack(data);
      }
    }
  };

  const deleteTrack = async (trackId) => {
    if (confirm('Are you sure you want to delete this track?')) {
      const res = await fetch(`${API_BASE_URL}/tracks/${trackId}`, {
        method: 'DELETE'
      });
      
      if (res.ok) {
        fetchTracks();
        if (selectedTrack?.id === trackId) {
          setSelectedTrack(null);
          setViewMode(null);
        }
      }
    }
  };

  const handleViewTrack = async (track) => {
    const res = await fetch(`${API_BASE_URL}/tracks/${track.id}`);
    const data = await res.json();
    setSelectedTrack(data);
    setViewMode('view');
  };

  const handleEditTrack = async (track) => {
    const res = await fetch(`${API_BASE_URL}/tracks/${track.id}`);
    const data = await res.json();
    setSelectedTrack(data);
    setEditForm({ 
      title: data.title, 
      artist_id: data.artist_id, 
      status_id: data.status_id 
    });
    setViewMode('edit');
  };

  const updateTrack = async () => {
    const res = await fetch(`${API_BASE_URL}/tracks/${selectedTrack.id}`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(editForm)
    });
    
    if (res.ok) {
      fetchTracks();
      const updated = await fetch(`${API_BASE_URL}/tracks/${selectedTrack.id}`);
      const data = await updated.json();
      setSelectedTrack(data);
      setViewMode('view');
    }
  };

  const cancelEdit = () => {
    setViewMode('view');
  };

  const createTag = async (e) => {
    e.preventDefault();
    const res = await fetch(`${API_BASE_URL}/tags`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name: newTag })
    });
    
    if (res.ok) {
      setNewTag('');
      setShowTagForm(false);
      fetchTags();
    }
  };

  const handleFilterClick = (filterType, filterValue) => {
    let filtered;
    if (filterType === 'status') {
      filtered = tracks.filter(t => t.status_id === filterValue);
    } else if (filterType === 'tag') {
      filtered = tracks.filter(t => t.tags?.some(tag => tag.id === filterValue));
    }
    setFilteredTracks(filtered);
    setViewMode('filter');
    setActiveFilter({ type: filterType, value: filterValue });
  };

  const getFilteredList = () => {
    return tracks
      .filter(track => 
        track.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
        track.artist?.name.toLowerCase().includes(searchQuery.toLowerCase())
      )
      .sort((a, b) => new Date(b.updated_at) - new Date(a.updated_at));
  };

  return (
    <div style={{ height: '100vh', display: 'flex', flexDirection: 'column', background: '#1a1a1a' }}>
      {/* Top Bar */}
      <div style={{ 
        padding: '15px 20px', 
        background: '#0a0a0a',
        borderBottom: '2px solid #4a3f2a',
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center'
      }}>
        <h1 style={{ margin: 0, display: 'flex', alignItems: 'center', gap: '10px', fontSize: '24px' }}>
          <Music size={28} />
          Tracks Manager
        </h1>
        
        <div style={{ display: 'flex', gap: '10px' }}>
          <button onClick={() => setShowArtistForm(!showArtistForm)} style={{
            padding: '8px 16px',
            fontSize: '14px',
            background: '#4a3f2a',
            color: '#fff',
            border: 'none',
            borderRadius: '5px',
            cursor: 'pointer'
          }}>
            + Artist
          </button>
          <button onClick={() => setShowTagForm(!showTagForm)} style={{
            padding: '8px 16px',
            fontSize: '14px',
            background: '#4a3f2a',
            color: '#fff',
            border: 'none',
            borderRadius: '5px',
            cursor: 'pointer'
          }}>
            + Tag
          </button>
        </div>
      </div>

      {/* Forms Section */}
      {(showArtistForm || showTagForm) && (
        <div style={{ padding: '15px 20px', background: '#0f0f0f', borderBottom: '1px solid #333' }}>
          {showArtistForm && (
            <form onSubmit={createArtist} style={{ display: 'flex', gap: '10px', marginBottom: showTagForm ? '10px' : 0 }}>
              <input
                type="text"
                placeholder="New Artist Name"
                value={newArtist}
                onChange={(e) => setNewArtist(e.target.value)}
                style={{ padding: '8px', fontSize: '14px', flex: 1, background: '#1a1a1a', color: '#fff', border: '1px solid #4a3f2a', borderRadius: '4px' }}
                required
              />
              <button type="submit" style={{
                padding: '8px 16px',
                fontSize: '14px',
                background: '#4a3f2a',
                color: '#fff',
                border: 'none',
                borderRadius: '4px',
                cursor: 'pointer'
              }}>
                Create
              </button>
              <button type="button" onClick={() => setShowArtistForm(false)} style={{
                padding: '8px 16px',
                fontSize: '14px',
                background: '#666',
                color: '#fff',
                border: 'none',
                borderRadius: '4px',
                cursor: 'pointer'
              }}>
                Cancel
              </button>
            </form>
          )}
          
          {showTagForm && (
            <form onSubmit={createTag} style={{ display: 'flex', gap: '10px' }}>
              <input
                type="text"
                placeholder="New Tag Name"
                value={newTag}
                onChange={(e) => setNewTag(e.target.value)}
                style={{ padding: '8px', fontSize: '14px', flex: 1, background: '#1a1a1a', color: '#fff', border: '1px solid #4a3f2a', borderRadius: '4px' }}
                required
              />
              <button type="submit" style={{
                padding: '8px 16px',
                fontSize: '14px',
                background: '#4a3f2a',
                color: '#fff',
                border: 'none',
                borderRadius: '4px',
                cursor: 'pointer'
              }}>
                Create
              </button>
              <button type="button" onClick={() => setShowTagForm(false)} style={{
                padding: '8px 16px',
                fontSize: '14px',
                background: '#666',
                color: '#fff',
                border: 'none',
                borderRadius: '4px',
                cursor: 'pointer'
              }}>
                Cancel
              </button>
            </form>
          )}
        </div>
      )}

      {/* Main Content - Split View */}
      <div style={{ flex: 1, display: 'flex', overflow: 'hidden' }}>
        {/* Left Panel - Compact List */}
        <div style={{ 
          width: '55%', 
          borderRight: '2px solid #4a3f2a',
          display: 'flex',
          flexDirection: 'column',
          background: '#0f0f0f'
        }}>
          {/* Search Bar */}
          <div style={{ padding: '15px' }}>
            <div style={{ position: 'relative' }}>
              <Search size={16} style={{ position: 'absolute', left: '12px', top: '50%', transform: 'translateY(-50%)', color: '#888' }} />
              <input
                type="text"
                placeholder="Search tracks or artists..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                autoFocus
                style={{
                  width: '100%',
                  padding: '10px 10px 10px 40px',
                  fontSize: '14px',
                  borderRadius: '8px',
                  border: '2px solid #4a3f2a',
                  background: '#1a1a1a',
                  color: '#fff',
                  boxSizing: 'border-box'
                }}
              />
            </div>
          </div>

          {/* Status Filter Pills */}
          <div style={{ 
            padding: '0 15px 10px 15px',
            display: 'flex',
            gap: '6px',
            flexWrap: 'wrap',
            borderBottom: '1px solid #333',
            paddingBottom: '15px'
          }}>
            {statuses.map(status => (
              <button
                key={status.id}
                onClick={() => handleFilterClick('status', status.id)}
                style={{
                  padding: '4px 10px',
                  fontSize: '11px',
                  background: getStatusColor(status.name),
                  color: '#fff',
                  border: 'none',
                  borderRadius: '12px',
                  cursor: 'pointer',
                  opacity: activeFilter?.type === 'status' && activeFilter?.value === status.id ? 1 : 0.6
                }}
              >
                {status.name}
              </button>
            ))}
          </div>

          {/* Track List */}
          <div style={{ flex: 1, overflowY: 'auto' }}>
            {getFilteredList().length === 0 ? (
              <p style={{ textAlign: 'center', color: '#888', marginTop: '40px' }}>
                No tracks found
              </p>
            ) : (
              getFilteredList().map(track => (
                <div
                  key={track.id}
                  style={{
                    padding: '12px 15px',
                    borderBottom: '1px solid #222',
                    background: selectedTrack?.id === track.id && viewMode !== 'filter' ? '#2c2416' : 'transparent',
                    display: 'flex',
                    alignItems: 'center',
                    gap: '12px',
                    transition: 'background 0.2s'
                  }}
                  onMouseEnter={(e) => {
                    if (selectedTrack?.id !== track.id || viewMode === 'filter') {
                      e.currentTarget.style.background = '#1a1a1a';
                    }
                  }}
                  onMouseLeave={(e) => {
                    if (selectedTrack?.id !== track.id || viewMode === 'filter') {
                      e.currentTarget.style.background = 'transparent';
                    }
                  }}
                >
                  {/* Title */}
                  <div style={{ flex: 1, minWidth: 0 }}>
                    <div style={{ fontWeight: 'bold', fontSize: '14px', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
                      {track.title}
                    </div>
                    <div style={{ fontSize: '11px', color: '#888' }}>
                      {track.artist?.name}
                    </div>
                  </div>

                  {/* Tags */}
                  <div style={{ display: 'flex', gap: '4px', flexWrap: 'wrap', maxWidth: '300px' }}>
                    {track.tags?.slice(0, 3).map(tag => (
                      <span
                        key={tag.id}
                        onClick={() => handleFilterClick('tag', tag.id)}
                        style={{
                          padding: '2px 6px',
                          borderRadius: '10px',
                          fontSize: '10px',
                          background: '#444',
                          color: '#fff',
                          cursor: 'pointer',
                          whiteSpace: 'nowrap'
                        }}
                      >
                        {tag.name}
                      </span>
                    ))}
                    {track.tags?.length > 3 && (
                      <span style={{ fontSize: '10px', color: '#888' }}>
                        +{track.tags.length - 3}
                      </span>
                    )}
                  </div>

                  {/* Action Buttons */}
                  <div style={{ display: 'flex', gap: '6px' }}>
                    <button
                      onClick={() => handleViewTrack(track)}
                      style={{
                        background: '#4a3f2a',
                        color: '#fff',
                        border: 'none',
                        padding: '6px 10px',
                        borderRadius: '4px',
                        cursor: 'pointer',
                        fontSize: '11px',
                        display: 'flex',
                        alignItems: 'center',
                        gap: '4px'
                      }}
                    >
                      <Eye size={12} /> View
                    </button>
                    <button
                      onClick={() => handleEditTrack(track)}
                      style={{
                        background: '#666',
                        color: '#fff',
                        border: 'none',
                        padding: '6px 10px',
                        borderRadius: '4px',
                        cursor: 'pointer',
                        fontSize: '11px',
                        display: 'flex',
                        alignItems: 'center',
                        gap: '4px'
                      }}
                    >
                      <Edit size={12} /> Edit
                    </button>
                    <button
                      onClick={() => deleteTrack(track.id)}
                      style={{
                        background: '#8b0000',
                        color: '#fff',
                        border: 'none',
                        padding: '6px 10px',
                        borderRadius: '4px',
                        cursor: 'pointer',
                        fontSize: '11px',
                        display: 'flex',
                        alignItems: 'center',
                        gap: '4px'
                      }}
                    >
                      <Trash2 size={12} /> Delete
                    </button>
                  </div>
                </div>
              ))
            )}
          </div>

          {/* Create Track Form */}
          <div style={{ padding: '15px', borderTop: '2px solid #333', background: '#0a0a0a' }}>
            <form onSubmit={createTrack} style={{ display: 'flex', gap: '8px' }}>
              <input
                type="text"
                placeholder="Track Title"
                value={newTrack.title}
                onChange={(e) => setNewTrack({...newTrack, title: e.target.value})}
                style={{ padding: '8px', fontSize: '13px', background: '#1a1a1a', color: '#fff', border: '1px solid #4a3f2a', borderRadius: '4px', flex: 1 }}
                required
              />
              <select
                value={newTrack.artist_id}
                onChange={(e) => setNewTrack({...newTrack, artist_id: e.target.value})}
                style={{ padding: '8px', fontSize: '13px', background: '#1a1a1a', color: '#fff', border: '1px solid #4a3f2a', borderRadius: '4px' }}
                required
              >
                <option value="">Artist</option>
                {artists.map(artist => (
                  <option key={artist.id} value={artist.id}>{artist.name}</option>
                ))}
              </select>
              <select
                value={newTrack.status_id}
                onChange={(e) => setNewTrack({...newTrack, status_id: e.target.value})}
                style={{ padding: '8px', fontSize: '13px', background: '#1a1a1a', color: '#fff', border: '1px solid #4a3f2a', borderRadius: '4px' }}
                required
              >
                <option value="">Status</option>
                {statuses.map(status => (
                  <option key={status.id} value={status.id}>{status.name}</option>
                ))}
              </select>
              <button type="submit" style={{
                padding: '8px 16px',
                fontSize: '13px',
                background: '#4a3f2a',
                color: '#fff',
                border: 'none',
                borderRadius: '4px',
                cursor: 'pointer',
                fontWeight: 'bold'
              }}>
                + Create
              </button>
            </form>
          </div>
        </div>

        {/* Right Panel - Dynamic View */}
        <div style={{ 
          flex: 1, 
          overflowY: 'auto',
          padding: '30px',
          background: '#1a1a1a'
        }}>
          {!viewMode ? (
            <div style={{ 
              textAlign: 'center', 
              color: '#666', 
              marginTop: '100px',
              fontSize: '18px'
            }}>
              <Music size={64} style={{ opacity: 0.3, marginBottom: '20px' }} />
              <div>Select a track to view or edit</div>
              <div style={{ fontSize: '14px', marginTop: '10px' }}>Or click a filter to see multiple tracks</div>
            </div>
          ) : viewMode === 'filter' ? (
            // FILTER VIEW - Multiple tracks condensed
            <div>
              <h2 style={{ fontSize: '24px', marginBottom: '20px', display: 'flex', alignItems: 'center', gap: '10px' }}>
                <Filter size={24} /> Filtered Tracks ({filteredTracks.length})
              </h2>
              <div style={{ display: 'grid', gap: '15px' }}>
                {filteredTracks.map(track => (
                  <div key={track.id} style={{
                    padding: '15px',
                    background: '#0f0f0f',
                    border: '1px solid #333',
                    borderRadius: '8px'
                  }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start', marginBottom: '10px' }}>
                      <div>
                        <h3 style={{ fontSize: '18px', margin: 0, marginBottom: '5px' }}>{track.title}</h3>
                        <div style={{ fontSize: '14px', color: '#888' }}>{track.artist?.name}</div>
                      </div>
                      <span style={{
                        padding: '4px 12px',
                        borderRadius: '12px',
                        fontSize: '12px',
                        background: getStatusColor(track.status?.name),
                        color: '#fff',
                        fontWeight: 'bold'
                      }}>
                        {track.status?.name}
                      </span>
                    </div>

                    {/* Tags */}
                    <div style={{ marginBottom: '10px' }}>
                      <div style={{ fontSize: '12px', color: '#999', marginBottom: '6px' }}>Tags:</div>
                      <div style={{ display: 'flex', flexWrap: 'wrap', gap: '6px' }}>
                        {track.tags?.map(tag => (
                          <span key={tag.id} style={{
                            background: '#444',
                            padding: '4px 8px',
                            borderRadius: '12px',
                            fontSize: '11px'
                          }}>
                            {tag.name}
                          </span>
                        ))}
                        <select 
                          onChange={(e) => {
                            if (e.target.value) {
                              addTagToTrack(track.id, e.target.value);
                              e.target.value = '';
                            }
                          }}
                          style={{
                            padding: '4px 8px',
                            background: '#4a3f2a',
                            color: '#fff',
                            border: 'none',
                            borderRadius: '12px',
                            cursor: 'pointer',
                            fontSize: '11px'
                          }}
                        >
                          <option value="">+ Add</option>
                          {tags.filter(tag => !track.tags?.find(t => t.id === tag.id)).map(tag => (
                            <option key={tag.id} value={tag.id}>{tag.name}</option>
                          ))}
                        </select>
                      </div>
                    </div>

                    {/* Links */}
                    <div>
                      <div style={{ fontSize: '12px', color: '#999', marginBottom: '6px' }}>Links: {track.links?.length || 0}</div>
                      {showLinkForm === track.id ? (
                        <div style={{ display: 'flex', gap: '6px', marginTop: '8px' }}>
                          <input
                            type="text"
                            placeholder="Type"
                            value={newLink.link_type}
                            onChange={(e) => setNewLink({...newLink, link_type: e.target.value})}
                            style={{ padding: '6px', fontSize: '12px', background: '#1a1a1a', color: '#fff', border: '1px solid #4a3f2a', borderRadius: '4px', width: '100px' }}
                          />
                          <input
                            type="url"
                            placeholder="URL"
                            value={newLink.link_url}
                            onChange={(e) => setNewLink({...newLink, link_url: e.target.value})}
                            style={{ padding: '6px', fontSize: '12px', background: '#1a1a1a', color: '#fff', border: '1px solid #4a3f2a', borderRadius: '4px', flex: 1 }}
                          />
                          <button onClick={() => addLinkToTrack(track.id)} style={{ padding: '6px 12px', fontSize: '12px', background: '#4a3f2a', color: '#fff', border: 'none', borderRadius: '4px', cursor: 'pointer' }}>
                            Add
                          </button>
                          <button onClick={() => setShowLinkForm(null)} style={{ padding: '6px 12px', fontSize: '12px', background: '#666', color: '#fff', border: 'none', borderRadius: '4px', cursor: 'pointer' }}>
                            Cancel
                          </button>
                        </div>
                      ) : (
                        <button onClick={() => setShowLinkForm(track.id)} style={{ padding: '6px 12px', fontSize: '12px', background: '#4a3f2a', color: '#fff', border: 'none', borderRadius: '4px', cursor: 'pointer', marginTop: '6px' }}>
                          + Add Link
                        </button>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          ) : viewMode === 'view' ? (
            // VIEW MODE - Single track, can add metadata
            <div>
              <div style={{ marginBottom: '30px' }}>
                <h2 style={{ fontSize: '32px', margin: 0, marginBottom: '10px' }}>{selectedTrack.title}</h2>
                <div style={{ fontSize: '18px', color: '#999', marginBottom: '15px' }}>
                  by {selectedTrack.artist?.name}
                </div>
                <span style={{
                  padding: '6px 16px',
                  borderRadius: '20px',
                  fontSize: '14px',
                  background: getStatusColor(selectedTrack.status?.name),
                  color: '#fff',
                  fontWeight: 'bold',
                  display: 'inline-block'
                }}>
                  {selectedTrack.status?.name}
                </span>
              </div>

              {/* Tags Section */}
              <div style={{ marginBottom: '30px' }}>
                <h3 style={{ fontSize: '18px', marginBottom: '12px' }}>Tags</h3>
                <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px' }}>
                  {selectedTrack.tags?.map(tag => (
                    <span 
                      key={tag.id} 
                      onClick={() => removeTagFromTrack(selectedTrack.id, tag.id)}
                      style={{
                        background: '#444',
                        padding: '6px 12px',
                        borderRadius: '16px',
                        cursor: 'pointer',
                        fontSize: '13px'
                      }}
                      title="Click to remove"
                    >
                      {tag.name} ✕
                    </span>
                  ))}
                  <select 
                    onChange={(e) => {
                      if (e.target.value) {
                        addTagToTrack(selectedTrack.id, e.target.value);
                        e.target.value = '';
                      }
                    }}
                    style={{
                      padding: '6px 12px',
                      background: '#4a3f2a',
                      color: '#fff',
                      border: 'none',
                      borderRadius: '16px',
                      cursor: 'pointer',
                      fontSize: '13px'
                    }}
                  >
                    <option value="">+ Add Tag</option>
                    {tags.filter(tag => !selectedTrack.tags?.find(t => t.id === tag.id)).map(tag => (
                      <option key={tag.id} value={tag.id}>{tag.name}</option>
                    ))}
                  </select>
                </div>
              </div>

              {/* Links Section */}
              <div>
                <h3 style={{ fontSize: '18px', marginBottom: '12px' }}>Links</h3>
                {selectedTrack.links?.map(link => (
                  <div key={link.id} style={{ 
                    display: 'flex',
                    alignItems: 'center',
                    gap: '12px',
                    marginBottom: '10px',
                    padding: '12px',
                    background: '#0f0f0f',
                    borderRadius: '8px',
                    border: '1px solid #333'
                  }}>
                    <div style={{ color: '#4a3f2a' }}>
                      {getLinkIcon(link.link_type)}
                    </div>
                    <span style={{ fontWeight: 'bold', minWidth: '100px', fontSize: '14px' }}>
                      {link.link_type}
                    </span>
                    <a 
                      href={link.link_url} 
                      target="_blank" 
                      rel="noopener noreferrer" 
                      style={{ 
                        color: '#4a9eff',
                        textDecoration: 'none',
                        fontSize: '14px',
                        flex: 1
                      }}
                    >
                      View Link <ExternalLink size={12} style={{ display: 'inline' }} />
                    </a>
                    <button 
                      onClick={() => removeLink(link.id)}
                      style={{
                        background: 'transparent',
                        color: '#8b0000',
                        border: 'none',
                        cursor: 'pointer',
                        fontSize: '16px'
                      }}
                    >
                      ✕
                    </button>
                  </div>
                ))}
                
                {showLinkForm === selectedTrack.id ? (
                  <div style={{ 
                    marginTop: '15px', 
                    padding: '15px',
                    background: '#0f0f0f',
                    borderRadius: '8px',
                    border: '2px solid #4a3f2a'
                  }}>
                    <input
                      type="text"
                      placeholder="Link Type (e.g., Spotify)"
                      value={newLink.link_type}
                      onChange={(e) => setNewLink({...newLink, link_type: e.target.value})}
                      style={{ 
                        padding: '10px', 
                        marginBottom: '10px',
                        width: '100%',
                        background: '#1a1a1a',
                        color: '#fff',
                        border: '1px solid #4a3f2a',
                        borderRadius: '6px',
                        boxSizing: 'border-box'
                      }}
                    />
                    <input
                      type="url"
                      placeholder="URL"
                      value={newLink.link_url}
                      onChange={(e) => setNewLink({...newLink, link_url: e.target.value})}
                      style={{ 
                        padding: '10px',
                        marginBottom: '10px',
                        width: '100%',
                        background: '#1a1a1a',
                        color: '#fff',
                        border: '1px solid #4a3f2a',
                        borderRadius: '6px',
                        boxSizing: 'border-box'
                      }}
                    />
                    <div style={{ display: 'flex', gap: '10px' }}>
                      <button
                        onClick={() => addLinkToTrack(selectedTrack.id)}
                        style={{
                          background: '#4a3f2a',
                          color: '#fff',
                          border: 'none',
                          padding: '10px 20px',
                          borderRadius: '6px',
                          cursor: 'pointer'
                        }}
                      >
                        Add Link
                      </button>
                      <button
                        onClick={() => {
                          setShowLinkForm(null);
                          setNewLink({ link_type: '', link_url: '' });
                        }}
                        style={{
                          background: '#666',
                          color: '#fff',
                          border: 'none',
                          padding: '10px 20px',
                          borderRadius: '6px',
                          cursor: 'pointer'
                        }}
                      >
                        Cancel
                      </button>
                    </div>
                  </div>
                ) : (
                  <button
                    onClick={() => setShowLinkForm(selectedTrack.id)}
                    style={{
                      background: '#4a3f2a',
                      color: '#fff',
                      border: 'none',
                      padding: '10px 20px',
                      borderRadius: '6px',
                      cursor: 'pointer',
                      marginTop: '10px'
                    }}
                  >
                    + Add Link
                  </button>
                )}
              </div>
            </div>
          ) : (
            // EDIT MODE - Single track, can change everything
            <div>
              <h2 style={{ fontSize: '24px', marginBottom: '20px' }}>Edit Track</h2>
              
              <div style={{ marginBottom: '20px' }}>
                <label style={{ display: 'block', marginBottom: '8px', fontSize: '14px', color: '#999' }}>Title</label>
                <input
                  type="text"
                  value={editForm.title}
                  onChange={(e) => setEditForm({...editForm, title: e.target.value})}
                  style={{ 
                    padding: '12px', 
                    fontSize: '16px',
                    width: '100%',
                    background: '#0f0f0f',
                    color: '#fff',
                    border: '2px solid #4a3f2a',
                    borderRadius: '8px',
                    boxSizing: 'border-box'
                  }}
                />
              </div>

              <div style={{ marginBottom: '20px' }}>
                <label style={{ display: 'block', marginBottom: '8px', fontSize: '14px', color: '#999' }}>Artist</label>
                <select
                  value={editForm.artist_id}
                  onChange={(e) => setEditForm({...editForm, artist_id: e.target.value})}
                  style={{ 
                    padding: '12px', 
                    fontSize: '16px',
                    width: '100%',
                    background: '#0f0f0f',
                    color: '#fff',
                    border: '2px solid #4a3f2a',
                    borderRadius: '8px',
                    boxSizing: 'border-box'
                  }}
                >
                  {artists.map(artist => (
                    <option key={artist.id} value={artist.id}>{artist.name}</option>
                  ))}
                </select>
              </div>

              <div style={{ marginBottom: '30px' }}>
                <label style={{ display: 'block', marginBottom: '8px', fontSize: '14px', color: '#999' }}>Status</label>
                <select
                  value={editForm.status_id}
                  onChange={(e) => setEditForm({...editForm, status_id: e.target.value})}
                  style={{ 
                    padding: '12px', 
                    fontSize: '16px',
                    width: '100%',
                    background: '#0f0f0f',
                    color: '#fff',
                    border: '2px solid #4a3f2a',
                    borderRadius: '8px',
                    boxSizing: 'border-box'
                  }}
                >
                  {statuses.map(status => (
                    <option key={status.id} value={status.id}>{status.name}</option>
                  ))}
                </select>
              </div>

              <div style={{ display: 'flex', gap: '10px' }}>
                <button
                  onClick={updateTrack}
                  style={{
                    background: '#4a3f2a',
                    color: '#fff',
                    border: 'none',
                    padding: '12px 24px',
                    borderRadius: '6px',
                    cursor: 'pointer',
                    fontWeight: 'bold',
                    fontSize: '14px'
                  }}
                >
                  Save Changes
                </button>
                <button
                  onClick={cancelEdit}
                  style={{
                    background: '#666',
                    color: '#fff',
                    border: 'none',
                    padding: '12px 24px',
                    borderRadius: '6px',
                    cursor: 'pointer',
                    fontSize: '14px'
                  }}
                >
                  Cancel
                </button>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default TracksManager;