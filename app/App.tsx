import React, { FC, useEffect } from 'react'

import { Empty } from '@00-team/utils'

import loadable from '@loadable/component'
import Navbar from 'layout/Navbar'
import { Route, Routes } from 'react-router-dom'

import { useAtom, useSetAtom } from 'jotai'
import { LocaleAtom, LocalesListAtom } from 'state'

import './style/base.scss'
import './style/fonts/imports.scss'

const Home = loadable(() => import('Home'))
const ErrorPage = loadable(() => import('layout/Error'))

const App: FC = () => {
    const [Locale, UpdateLocale] = useAtom(LocaleAtom)
    const UpdateLocalesList = useSetAtom(LocalesListAtom)

    useEffect(() => {
        UpdateLocale()
        UpdateLocalesList()
    }, [])

    useEffect(() => {
        if (Locale.direction) {
            const right = Locale.direction === 'rtl'
            document.body.style.direction = right ? 'rtl' : 'ltr'
            document.body.style.textAlign = right ? 'right' : 'left'
        }
    }, [Locale])

    if (Empty(Locale)) return <div>Loading...</div>

    return (
        <>
            <Navbar />
            <MainContent />
        </>
    )
}

const MainContent: FC = () => {
    if (typeof ERROR !== 'undefined') return <ErrorPage {...ERROR} />

    return (
        <Routes>
            <Route index element={<Home />} />
        </Routes>
    )
}

export default App
