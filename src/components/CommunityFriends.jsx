import { useEffect, useState } from 'react';
import { Check, Clock, Loader2, MessageCircle, UserCheck, UserPlus, Users, X } from 'lucide-react';
import { apiRequest } from '../lib/api';
import { Avatar, EmptyState, SearchField } from './SocialUI';
import { Button } from './ui/button';
import { Dialog, DialogContent, DialogDescription, DialogTitle } from './ui/dialog';

export function useFriends() {
  const [friends, setFriends] = useState([]);
  const [incomingRequests, setIncomingRequests] = useState([]);
  const [outgoingRequests, setOutgoingRequests] = useState([]);
  const [busy, setBusy] = useState(true);
  const [error, setError] = useState('');
  const [version, setVersion] = useState(0);

  useEffect(() => {
    let cancelled = false;
    setBusy(true);
    setError('');
    apiRequest('/api/friends')
      .then(data => {
        if (!cancelled) {
          setFriends(data.friends ?? []);
          setIncomingRequests(data.incomingRequests ?? []);
          setOutgoingRequests(data.outgoingRequests ?? []);
        }
      })
      .catch(err => {
        if (!cancelled) setError(err.message || 'Could not load friends.');
      })
      .finally(() => {
        if (!cancelled) setBusy(false);
      });
    return () => {
      cancelled = true;
    };
  }, [version]);

  const updateFromResponse = data => {
    if (data.friends) setFriends(data.friends);
    if (data.incomingRequests) setIncomingRequests(data.incomingRequests);
    if (data.outgoingRequests) setOutgoingRequests(data.outgoingRequests);
  };

  const sendRequest = async userId => {
    const data = await apiRequest('/api/friends/request', { method: 'POST', body: JSON.stringify({ userId }) });
    updateFromResponse(data);
    return data;
  };

  const acceptRequest = async (requestId, userId) => {
    const data = await apiRequest('/api/friends/accept', { method: 'POST', body: JSON.stringify({ requestId, userId }) });
    updateFromResponse(data);
    return data;
  };

  const declineRequest = async (requestId, userId) => {
    const data = await apiRequest('/api/friends/decline', { method: 'POST', body: JSON.stringify({ requestId, userId }) });
    updateFromResponse(data);
    return data;
  };

  const cancelRequest = async (requestId, userId) => {
    const data = await apiRequest('/api/friends/cancel', { method: 'POST', body: JSON.stringify({ requestId, userId }) });
    updateFromResponse(data);
    return data;
  };

  return {
    friends,
    incomingRequests,
    outgoingRequests,
    busy,
    error,
    add: sendRequest,
    sendRequest,
    acceptRequest,
    declineRequest,
    cancelRequest,
    retry: () => setVersion(value => value + 1),
  };
}

export function AddFriendDialog({ model, open, onOpenChange }) {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState('');
  const [adding, setAdding] = useState(null);
  const [notice, setNotice] = useState('');
  const [retry, setRetry] = useState(0);
  const term = query.trim();

  useEffect(() => {
    let cancelled = false;
    setResults([]);
    setError('');
    if (!open || term.length < 2) {
      setBusy(false);
      return;
    }
    setBusy(true);
    const timer = setTimeout(async () => {
      try {
        const data = await apiRequest(`/api/users/search?q=${encodeURIComponent(term)}`);
        if (!cancelled) setResults(data.users ?? []);
      } catch (err) {
        if (!cancelled) setError(err.message || 'Could not search users.');
      } finally {
        if (!cancelled) setBusy(false);
      }
    }, 250);
    return () => {
      cancelled = true;
      clearTimeout(timer);
    };
  }, [term, open, retry]);

  const sendReq = async person => {
    if (adding) return;
    setAdding(person.id);
    setNotice('');
    try {
      const res = await model.sendRequest(person.id);
      if (res.accepted) {
        setNotice(`You and ${person.name} are now friends!`);
      } else {
        setNotice(`Friend request sent to ${person.name}.`);
      }
    } catch (err) {
      setNotice(err.message || 'Could not send friend request. Please try again.');
    } finally {
      setAdding(null);
    }
  };

  const acceptIncoming = async (incomingReq, person) => {
    if (adding) return;
    setAdding(person.id);
    setNotice('');
    try {
      await model.acceptRequest(incomingReq.id, person.id);
      setNotice(`You and ${person.name} are now friends!`);
    } catch (err) {
      setNotice(err.message || 'Could not accept friend request.');
    } finally {
      setAdding(null);
    }
  };

  return (
    <Dialog
      open={open}
      onOpenChange={value => {
        onOpenChange(value);
        if (!value) {
          setQuery('');
          setNotice('');
        }
      }}
    >
      <DialogContent onOpenAutoFocus={e => e.preventDefault()}>
        <div className="mb-5 flex h-12 w-12 items-center justify-center rounded-2xl bg-teal-50 text-teal-800 dark:bg-teal-950 dark:text-teal-200">
          <UserPlus size={23} />
        </div>
        <DialogTitle>Add friend</DialogTitle>
        <DialogDescription>Find learners by name or college and send them a friend request.</DialogDescription>
        <div className="mt-5">
          <SearchField
            value={query}
            onChange={value => {
              setQuery(value);
              setResults([]);
              setNotice('');
            }}
            placeholder="Search users by name or college"
          />
        </div>
        {notice && (
          <p role="status" className="mt-3 rounded-lg bg-teal-50 p-3 text-sm text-teal-900 dark:bg-teal-950 dark:text-teal-100">
            {notice}
          </p>
        )}
        {model.error && (
          <p role="alert" className="mt-3 text-sm text-red-600 dark:text-red-400">
            {model.error}{' '}
            <button className="underline" onClick={model.retry}>
              Retry loading friends
            </button>
          </p>
        )}
        <div className="mt-3 max-h-80 overflow-y-auto">
          {term.length < 2 ? (
            <EmptyState icon={Users} title="Find your study partners">
              Type at least 2 characters to search for other users.
            </EmptyState>
          ) : busy ? (
            <p role="status" className="flex items-center justify-center gap-2 py-10 text-sm text-slate-500">
              <Loader2 size={17} className="motion-safe:animate-spin" />
              Searching users…
            </p>
          ) : error ? (
            <div role="alert" className="py-6 text-center text-sm text-red-600 dark:text-red-400">
              <p>{error}</p>
              <Button variant="ghost" className="mt-2" onClick={() => setRetry(value => value + 1)}>
                Try again
              </Button>
            </div>
          ) : results.length ? (
            <ul className="divide-y divide-slate-100 dark:divide-slate-800">
              {results.map(person => {
                const isFriend = model.friends.some(friend => friend.id === person.id);
                const hasPendingOut = (model.outgoingRequests ?? []).some(req => req.user?.id === person.id);
                const incomingReq = (model.incomingRequests ?? []).find(req => req.user?.id === person.id);
                const isProcessing = adding === person.id;

                return (
                  <li key={person.id} className="flex items-center gap-3 py-4">
                    <Avatar name={person.name} src={person.profileImageUrl} />
                    <div className="min-w-0 flex-1">
                      <p className="truncate text-sm font-semibold" title={person.name}>
                        {person.name}
                      </p>
                      <p className="mt-1 truncate text-xs text-slate-500 dark:text-slate-400" title={person.medicalCollege}>
                        {person.medicalCollege}
                      </p>
                    </div>

                    {isFriend ? (
                      <Button size="sm" variant="secondary" disabled className="gap-1 opacity-70">
                        <Check size={14} />
                        Friends
                      </Button>
                    ) : incomingReq ? (
                      <Button
                        size="sm"
                        disabled={isProcessing}
                        onClick={() => acceptIncoming(incomingReq, person)}
                        className="gap-1 bg-teal-800 text-white hover:bg-teal-900 dark:bg-teal-300 dark:text-teal-950"
                      >
                        {isProcessing ? <Loader2 size={14} className="motion-safe:animate-spin" /> : <Check size={14} />}
                        Accept
                      </Button>
                    ) : hasPendingOut ? (
                      <Button size="sm" variant="outline" disabled className="gap-1 opacity-75">
                        <Clock size={14} />
                        Requested
                      </Button>
                    ) : (
                      <Button
                        size="sm"
                        disabled={isProcessing || model.busy}
                        onClick={() => sendReq(person)}
                        aria-label={`Send friend request to ${person.name}`}
                        className="gap-1"
                      >
                        {isProcessing ? <Loader2 size={14} className="motion-safe:animate-spin" /> : <UserPlus size={14} />}
                        {isProcessing ? 'Sending…' : 'Add'}
                      </Button>
                    )}
                  </li>
                );
              })}
            </ul>
          ) : (
            <EmptyState icon={Users} title="No users found">
              Try another name or college.
            </EmptyState>
          )}
        </div>
      </DialogContent>
    </Dialog>
  );
}

export function FriendsPanel({ model, onAdd, onMessage }) {
  const [query, setQuery] = useState('');
  const [opening, setOpening] = useState(null);
  const visible = model.friends.filter(person =>
    `${person.name} ${person.medicalCollege}`.toLowerCase().includes(query.trim().toLowerCase()),
  );

  if (model.busy) {
    return (
      <p role="status" className="flex items-center gap-2 py-8 text-sm text-slate-500">
        <Loader2 size={16} className="motion-safe:animate-spin" />
        Loading friends…
      </p>
    );
  }

  if (model.error) {
    return (
      <div role="alert" className="rounded-xl border border-slate-200 p-5 dark:border-slate-800">
        <p className="text-sm">{model.error}</p>
        <Button variant="outline" className="mt-3" onClick={model.retry}>
          Try again
        </Button>
      </div>
    );
  }

  if (!model.friends.length) {
    return (
      <div className="rounded-2xl border border-dashed border-slate-200 bg-white dark:border-slate-800 dark:bg-slate-900">
        <EmptyState icon={Users} title="Your study circle starts with a friend">
          Find other learners and keep your study partners close.
          <div>
            <Button className="mt-4" onClick={onAdd}>
              <UserPlus size={15} />
              Find friends
            </Button>
          </div>
        </EmptyState>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      <SearchField value={query} onChange={setQuery} placeholder="Search your friends" />
      <div className="grid gap-3 sm:grid-cols-2">
        {visible.map(person => (
          <article
            key={person.id}
            className="flex min-w-0 items-center gap-3 rounded-2xl border border-slate-200 bg-white p-4 dark:border-slate-800 dark:bg-slate-900"
          >
            <Avatar name={person.name} src={person.profileImageUrl} />
            <div className="min-w-0 flex-1">
              <h4 className="truncate text-sm font-semibold" title={person.name}>
                {person.name}
              </h4>
              <p className="mt-1 truncate text-xs text-slate-500 dark:text-slate-400" title={person.medicalCollege}>
                {person.medicalCollege}
              </p>
              <Button
                variant="ghost"
                size="sm"
                className="-ml-3 mt-1 text-teal-700 dark:text-teal-200"
                disabled={Boolean(opening)}
                onClick={async () => {
                  setOpening(person.id);
                  try {
                    await onMessage(person.id);
                  } finally {
                    setOpening(null);
                  }
                }}
              >
                <MessageCircle size={13} />
                {opening === person.id ? 'Opening…' : 'Message'}
              </Button>
            </div>
          </article>
        ))}
      </div>
      {!visible.length && <p role="status" className="py-6 text-center text-sm text-slate-500">No friends match your search.</p>}
    </div>
  );
}

export function RequestsPanel({ model, onAdd }) {
  const [processing, setProcessing] = useState(null);
  const [notice, setNotice] = useState('');

  const incoming = model.incomingRequests ?? [];
  const outgoing = model.outgoingRequests ?? [];

  const handleAccept = async req => {
    if (processing) return;
    setProcessing(`accept-${req.id}`);
    setNotice('');
    try {
      await model.acceptRequest(req.id, req.user?.id);
      setNotice(`You and ${req.user?.name} are now study friends!`);
    } catch (err) {
      setNotice(err.message || 'Could not accept request.');
    } finally {
      setProcessing(null);
    }
  };

  const handleDecline = async req => {
    if (processing) return;
    setProcessing(`decline-${req.id}`);
    setNotice('');
    try {
      await model.declineRequest(req.id, req.user?.id);
      setNotice(`Request from ${req.user?.name} declined.`);
    } catch (err) {
      setNotice(err.message || 'Could not decline request.');
    } finally {
      setProcessing(null);
    }
  };

  const handleCancel = async req => {
    if (processing) return;
    setProcessing(`cancel-${req.id}`);
    setNotice('');
    try {
      await model.cancelRequest(req.id, req.user?.id);
      setNotice(`Request to ${req.user?.name} cancelled.`);
    } catch (err) {
      setNotice(err.message || 'Could not cancel request.');
    } finally {
      setProcessing(null);
    }
  };

  if (model.busy) {
    return (
      <p role="status" className="flex items-center gap-2 py-8 text-sm text-slate-500">
        <Loader2 size={16} className="motion-safe:animate-spin" />
        Loading requests…
      </p>
    );
  }

  const hasRequests = incoming.length > 0 || outgoing.length > 0;

  if (!hasRequests) {
    return (
      <div className="rounded-2xl border border-dashed border-slate-200 bg-white dark:border-slate-800 dark:bg-slate-900">
        <EmptyState icon={UserCheck} title="No pending friend requests">
          When other learners send you a friend request, they’ll show up here. You can also search for friends to connect.
          <div>
            <Button className="mt-4" onClick={onAdd}>
              <UserPlus size={15} />
              Find friends
            </Button>
          </div>
        </EmptyState>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {notice && (
        <p role="status" className="rounded-lg bg-teal-50 p-3 text-sm text-teal-900 dark:bg-teal-950 dark:text-teal-100">
          {notice}
        </p>
      )}

      {/* Received Requests */}
      <div>
        <div className="mb-3 flex items-center justify-between">
          <h4 className="text-sm font-semibold text-slate-900 dark:text-slate-100">
            Received requests{' '}
            {incoming.length > 0 && (
              <span className="ml-1.5 rounded-full bg-teal-100 px-2 py-0.5 text-xs font-bold text-teal-800 dark:bg-teal-900/60 dark:text-teal-200">
                {incoming.length}
              </span>
            )}
          </h4>
        </div>
        {incoming.length === 0 ? (
          <p className="rounded-xl border border-slate-100 bg-slate-50/50 p-4 text-xs text-slate-500 dark:border-slate-800 dark:bg-slate-900/50">
            No incoming friend requests.
          </p>
        ) : (
          <div className="grid gap-3 sm:grid-cols-2">
            {incoming.map(req => {
              const person = req.user;
              const isAccepting = processing === `accept-${req.id}`;
              const isDeclining = processing === `decline-${req.id}`;
              return (
                <article
                  key={req.id}
                  className="flex min-w-0 flex-col justify-between rounded-2xl border border-slate-200 bg-white p-4 dark:border-slate-800 dark:bg-slate-900"
                >
                  <div className="flex min-w-0 items-center gap-3">
                    <Avatar name={person.name} src={person.profileImageUrl} />
                    <div className="min-w-0 flex-1">
                      <h5 className="truncate text-sm font-semibold" title={person.name}>
                        {person.name}
                      </h5>
                      <p className="mt-0.5 truncate text-xs text-slate-500 dark:text-slate-400" title={person.medicalCollege}>
                        {person.medicalCollege}
                      </p>
                    </div>
                  </div>
                  <div className="mt-4 flex items-center gap-2 border-t border-slate-100 pt-3 dark:border-slate-800">
                    <Button
                      size="sm"
                      className="flex-1 bg-teal-800 text-white hover:bg-teal-900 dark:bg-teal-300 dark:text-teal-950 dark:hover:bg-teal-200"
                      disabled={Boolean(processing)}
                      onClick={() => handleAccept(req)}
                    >
                      {isAccepting ? <Loader2 size={14} className="motion-safe:animate-spin" /> : <Check size={14} />}
                      {isAccepting ? 'Accepting…' : 'Accept'}
                    </Button>
                    <Button
                      size="sm"
                      variant="outline"
                      className="flex-1"
                      disabled={Boolean(processing)}
                      onClick={() => handleDecline(req)}
                    >
                      {isDeclining ? <Loader2 size={14} className="motion-safe:animate-spin" /> : <X size={14} />}
                      {isDeclining ? 'Declining…' : 'Decline'}
                    </Button>
                  </div>
                </article>
              );
            })}
          </div>
        )}
      </div>

      {/* Sent Requests */}
      <div>
        <div className="mb-3 flex items-center justify-between">
          <h4 className="text-sm font-semibold text-slate-900 dark:text-slate-100">
            Sent requests{' '}
            {outgoing.length > 0 && (
              <span className="ml-1.5 rounded-full bg-slate-100 px-2 py-0.5 text-xs font-semibold text-slate-600 dark:bg-slate-800 dark:text-slate-300">
                {outgoing.length}
              </span>
            )}
          </h4>
        </div>
        {outgoing.length === 0 ? (
          <p className="rounded-xl border border-slate-100 bg-slate-50/50 p-4 text-xs text-slate-500 dark:border-slate-800 dark:bg-slate-900/50">
            No outgoing friend requests.
          </p>
        ) : (
          <div className="grid gap-3 sm:grid-cols-2">
            {outgoing.map(req => {
              const person = req.user;
              const isCancelling = processing === `cancel-${req.id}`;
              return (
                <article
                  key={req.id}
                  className="flex min-w-0 items-center justify-between gap-3 rounded-2xl border border-slate-200 bg-white p-4 dark:border-slate-800 dark:bg-slate-900"
                >
                  <div className="flex min-w-0 items-center gap-3">
                    <Avatar name={person.name} src={person.profileImageUrl} />
                    <div className="min-w-0 flex-1">
                      <h5 className="truncate text-sm font-semibold" title={person.name}>
                        {person.name}
                      </h5>
                      <p className="mt-0.5 truncate text-xs text-slate-500 dark:text-slate-400" title={person.medicalCollege}>
                        {person.medicalCollege}
                      </p>
                      <span className="mt-1 inline-block text-[11px] font-medium text-amber-600 dark:text-amber-400">
                        Request pending…
                      </span>
                    </div>
                  </div>
                  <Button
                    size="sm"
                    variant="ghost"
                    className="text-xs text-slate-500 hover:text-red-600 dark:hover:text-red-400"
                    disabled={Boolean(processing)}
                    onClick={() => handleCancel(req)}
                  >
                    {isCancelling ? <Loader2 size={13} className="motion-safe:animate-spin" /> : 'Cancel'}
                  </Button>
                </article>
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
}
